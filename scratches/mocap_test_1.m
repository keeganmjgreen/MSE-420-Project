myVideoReader = VideoReader('xylophone.mp4');

myVideo = read(myVideoReader);
                           %, myVideoReader.FrameRate * [StartTime, EndTime]);

myVideoReader.CurrentTime = 0.6; % StartTime;

while myVideoReader.CurrentTime <= 0.9 % EndTime
    myFrame = readFrame(myVideoReader);
end
