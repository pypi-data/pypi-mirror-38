/*
 * Copyright 2018 Fairtide Pte. Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <signal.h>
#include <atomic>
#include <chrono>
#include <type_traits>

#include <boost/program_options.hpp>

#include <AeronArchive.h>
#include <ChannelUri.h>
#include <RecordingPos.h>

#include "SamplesUtil.h"

namespace po = boost::program_options;
namespace codecs = io::aeron::archive::codecs;

using namespace aeron;

namespace {
std::atomic<bool> running{true};

void sigIntHandler(int) { running = false; }

std::int32_t positionBitsToShift(std::int32_t termBufferLength) {
    switch (termBufferLength) {
        case 64 * 1024:
            return 16;
        case 128 * 1024:
            return 17;
        case 256 * 1024:
            return 18;
        case 512 * 1024:
            return 19;
        case 1024 * 1024:
            return 20;
        case 2 * 1024 * 1024:
            return 21;
        case 4 * 1024 * 1024:
            return 22;
        case 8 * 1024 * 1024:
            return 23;
        case 16 * 1024 * 1024:
            return 24;
        case 32 * 1024 * 1024:
            return 25;
        case 64 * 1024 * 1024:
            return 26;
        case 128 * 1024 * 1024:
            return 27;
        case 256 * 1024 * 1024:
            return 28;
        case 512 * 1024 * 1024:
            return 29;
        case 1024 * 1024 * 1024:
            return 30;
    }

    throw util::IllegalArgumentException("Invalid term buffer length: " + std::to_string(termBufferLength), SOURCEINFO);
}

std::int32_t computeTermIdFromPosition(std::int64_t position, std::int32_t positionBitsToShift,
                                       std::int32_t initialTermId) {
    return (static_cast<std::int32_t>(position >> positionBitsToShift) + initialTermId);
}

}  // namespace

int main(int argc, char* argv[]) {
    ::signal(SIGINT, sigIntHandler);

    std::string channel, configFile;
    std::int32_t streamId, messagesCount;
    bool extendRecording;

    po::options_description desc("Options");
    desc.add_options()("help", "print help message")(
        "channel,c", po::value<std::string>(&channel)->default_value("aeron:udp?endpoint=localhost:40123"))(
        "stream-id,i", po::value<std::int32_t>(&streamId)->default_value(10))(
        "messages-count,m", po::value<std::int32_t>(&messagesCount)->default_value(1000000))(
        "extend-recording,e", po::bool_switch(&extendRecording)->default_value(false))(
        "file,f", po::value<std::string>(&configFile));

    try {
        po::variables_map vm;
        po::store(po::parse_command_line(argc, argv, desc), vm);
        po::notify(vm);

        if (vm.count("help")) {
            std::cout << desc << '\n';
            return 1;
        }

        std::cout << "Publishing to " << channel << " on stream id " << streamId << '\n';

        std::unique_ptr<aeron::archive::Configuration> cfg;

        if (!configFile.empty()) {
            cfg = std::make_unique<aeron::archive::Configuration>(configFile);
        } else {
            cfg = std::make_unique<aeron::archive::Configuration>();
        }

        aeron::archive::Context ctx(*cfg);
        auto archive = aeron::archive::AeronArchive::connect(ctx);
        auto aeron = archive->context().aeron();

        // get the latest recording ID and extend the recording
        auto recording = aeron::archive::getLatestRecordingData(*archive, channel, streamId);

        auto publishData = [&](auto publication) {
            // find an archiving counter
            std::cout << "Waiting for the counter...\n";

            auto& counters = aeron->countersReader();
            std::int32_t counterId = archive::RecordingPos::findCounterIdBySession(counters, publication->sessionId());

            while (-1 == counterId) {
                if (!running) {
                    return;
                }

                std::this_thread::yield();
                counterId = archive::RecordingPos::findCounterIdBySession(counters, publication->sessionId());
            }

            // wait for recording to start
            std::int64_t recordingId = archive::RecordingPos::getRecordingId(counters, counterId);
            std::cout << "Recording started, recording id = " << recordingId << '\n';

            // publish messages
            std::array<std::uint8_t, 256> buffer;
            concurrent::AtomicBuffer srcBuffer(buffer);
            char message[256];

            for (std::int32_t i = 0; i < messagesCount && running; ++i) {
                int messageLen = ::snprintf(message, sizeof(message), "Hello World! %d", i);
                srcBuffer.putBytes(0, reinterpret_cast<std::uint8_t*>(message), messageLen);

                std::cout << "offering " << i << "/" << messagesCount << " - ";

                std::int64_t result = publication->offer(srcBuffer, 0, messageLen);

                if (result < 0) {
                    if (BACK_PRESSURED == result) {
                        std::cout << "Offer failed due to back pressure\n";
                    } else if (NOT_CONNECTED == result) {
                        std::cout << "Offer failed because publisher is not connected to subscriber\n";
                    } else if (ADMIN_ACTION == result) {
                        std::cout << "Offer failed because of an administration action in the system\n";
                    } else if (PUBLICATION_CLOSED == result) {
                        std::cout << "Offer failed publication is closed\n";
                    } else {
                        std::cout << "Offer failed due to unknown reason" << result << std::endl;
                    }
                } else {
                    std::cout << "yay!\n";
                }

                //
                auto errorMessage = archive->pollForErrorResponse();
                if (errorMessage) {
                    throw util::IllegalStateException(*errorMessage, SOURCEINFO);
                }

                ::sleep(1);
            }

            // wait for recording to complete
            while (counters.getCounterValue(counterId) < publication->position()) {
                if (!archive::RecordingPos::isActive(counters, counterId, recording.recordingId)) {
                    std::cerr << "recording has stopped unexpectedly: " << recording.recordingId << '\n';
                    break;
                }

                std::this_thread::yield();
            }
        };

        if (extendRecording && recording.recordingId != -1) {
            std::shared_ptr<ExclusivePublication> publication;

            // rebuilding the channel
            std::int32_t bitsToShift = positionBitsToShift(recording.termBufferLength);
            std::int32_t termId =
                computeTermIdFromPosition(recording.stopPosition, bitsToShift, recording.initialTermId);
            std::int32_t termOffset = recording.stopPosition & (recording.termBufferLength - 1);

            std::ostringstream ss;
            ss << channel << "|init-term-id=" << recording.initialTermId
               << "|term-length=" << recording.termBufferLength << "|term-id=" << termId
               << "|term-offset=" << termOffset << "|mtu=1408";

            std::string extendChannel = ss.str();

            std::cout << "Extending recording " << recording.recordingId << ", new channel: " << extendChannel
                      << "...\n";

            std::int64_t pubId = aeron->addExclusivePublication(extendChannel, streamId);
            while (!(publication = aeron->findExclusivePublication(pubId))) {
                std::this_thread::yield();
            }

            archive->extendRecording(recording.recordingId, channel, streamId, codecs::SourceLocation::LOCAL);
            publishData(publication);
        } else {
            std::shared_ptr<Publication> publication;

            std::cout << "Starting new recording...\n";
            std::int64_t pubId = aeron->addPublication(channel, streamId);
            while (!(publication = aeron->findPublication(pubId))) {
                std::this_thread::yield();
            }

            archive->startRecording(channel, streamId, codecs::SourceLocation::LOCAL);
            publishData(publication);
        }

        archive->stopRecording(channel, streamId);

        std::cout << "Shutting down...\n";
    } catch (const archive::ArchiveException& e) {
        std::cerr << "aeron archive exception: " << e.what() << " (" << e.where() << ")\n" << '\n';
        return 1;
    } catch (const util::SourcedException& e) {
        std::cerr << "aeron exception: " << e.what() << " (" << e.where() << ")\n";
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "exception: " << e.what() << '\n';
        return 1;
    }

    std::cout << "done\n";

    return 0;
}
