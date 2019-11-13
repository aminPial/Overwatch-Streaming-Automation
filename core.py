import argparse, time, os, cv2, shutil, datetime, math, subprocess, pickle, multiprocessing
from actn import *

ap = argparse.ArgumentParser()

# for help -> python alpha.py --help

ap.add_argument("-f", "--file", required=True,
                help="name of the file")
ap.add_argument("-o", "--output", required=True,
                help="specifiy the folder path of output")
ap.add_argument("-b", "--before", required=True,
                help="seconds to cut before", type=int)
ap.add_argument("-a", "--after", required=True,
                help="seconds to cut after", type=int)

args = vars(ap.parse_args())


class core_overwatch():

    def __init__(self, file_name, output_folder, before, after):

        self.file_name = file_name
        self.output_folder = output_folder
        self.before = before
        self.after = after

        if not os.path.exists(str(self.output_folder)):
            print("The File Path Doesn't Exist!")
            print("[++++++]Creating the Folder in Path {0}".format(output_folder))
            os.makedirs("{0}".format(self.output_folder))
            print("[++++++]Finished Making The Folder in Path {0}".format(output_folder))

        try:
            fh = open('{0}'.format(self.file_name), 'r')

        except FileNotFoundError:
            print("[+++++++]The Video File Not Found In Path.Please Try Again")

        cmd1 = "ffmpeg -i {0} 2>&1 | sed -n \"s/.*, \(.*\) fp.*/\\1/p\"".format(self.file_name)

        os.system(cmd1 + ' >  tmp1')
        self.fps = int(open('tmp1', 'r').read())

        os.system(
            """ ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {0}  > tmp2 """.format(
                self.file_name
            ))
        self.frame_count = int(open('tmp2', 'r').read())

        print('[++++++]fps', self.fps)
        print('[++++++]frame count', self.frame_count)
        # get imp vid inf

    def build_folder(self):

        folder_names = ['./raw_calc', './raw_calc/frame_db_temp']

        for directory in folder_names:
            if not os.path.exists(str(directory)):
                os.makedirs(str(directory))

            # if exists then delete all the files in that dir tree

    def which_frame_formula(self):

        second_length = 1
        chunk_size = round(self.fps * second_length)  # fps*second_length

        assert type(chunk_size) is int, "Chunk Size must have to be Integer Type"

        # upto which frame the ops will execute(for loop to extract one frame from chunk size )
        n = round(round(self.frame_count) / chunk_size)

        start_frame = round(self.fps / 2)

        common_diff = round(self.fps * second_length)  # * second length,taking 1F/60

        return start_frame, n, common_diff

    def select_frame(self, a, n, d):
        # arithmetic series y=a+(p-1)*d

        which_frame_list = [a + (p - 1) * d for p in range(1, n + 1)]

        return which_frame_list

    def read_save_frame(self):

        os.system("ffmpeg -hide_banner -loglevel panic -i {video_Fname} -vf fps=1  {f_name}/%d.png".format(

            f_name='./raw_calc/frame_db_temp', video_Fname=str(self.file_name)
        ))

    def get_action_process_multithreaded_cmd_run_commands(self):

        img_list = ['./raw_calc/frame_db_temp/{0}'.format(x) for x in os.listdir('./raw_calc/frame_db_temp')]
        img_list.sort(key=lambda fx: int(''.join(filter(str.isdigit, fx))))

        az = return_text(img_list)

        return az

    # utils  function start here -3

    def _dbl(self, time):
        if time < 10:
            return '0' + str(time)
        else:
            return str(time)

    def time_cut(self, input_in_sec):

        times = []
        hours = 0
        minutes = 0
        seconds = 0

        hours = input_in_sec // 3600
        minutes = (input_in_sec % 3600) // 60
        seconds = (input_in_sec % 3600) % 60

        return "{}:{}:{}".format(core_overwatch._dbl(self, hours), core_overwatch._dbl(self, minutes),
                                 core_overwatch._dbl(self, seconds))

    def findIndices(self, sequence, _str, extra=0):  # 0011
        assert len(sequence) < len(_str), "Sequence is Greater Than the Main String"
        indices = []
        for i in range(len(_str) - len(sequence) + 1):
            temp = _str[i:i + len(sequence)]
            if (sequence == temp):
                indices.append(i + 2 - extra)

        return indices

    # utils fx ends here

    def action_index_find(self, raw_list, which_frame):

        raw_str_hashed = ''

        for j in raw_list:
            raw_str_hashed += str(j)

        assert type(raw_str_hashed) is str, " The parameter to find Indices Type must have to be a String"

        result_list = core_overwatch.findIndices(self, '01', raw_str_hashed, extra=1)

        final_result = []

        for yx in result_list:
            final_result.append(int(which_frame[yx]))

        return final_result

    def build_frame_range_to_cut(self, action_result):

        # print(action_result)

        # input will be taken ->cp from raw code
        frames = round(self.frame_count)
        fps = round(self.fps)

        bef = int(self.before) * fps  # count frm

        aft = int(self.after) * fps

        # frame range (tuple ds) contained list

        frame_range = []

        # build condition for after and before trimming

        for ucv in action_result:

            if int(ucv) < bef and aft < frames:

                frame_range.append((0, ucv + aft))

            elif int(ucv) < bef and aft > frames:

                frame_range.append((0, frames))

            elif int(ucv) > bef and aft < frames:

                frame_range.append((ucv - bef, ucv + aft))

            elif int(ucv) > bef and aft < frames:

                frame_range.append((ucv - bef, frames))

        # (temp) test

        return frame_range

    def build_output(self, start, end, video_name, file_name, end1):

        os.system(
            'ffmpeg -hide_banner -loglevel panic -ss {st} -i {ivfname} -to {ed} -c copy {ovfname}'.format(st=start,
                                                                                                          ed=end1,
                                                                                                          ivfname=self.file_name,
                                                                                                          ovfname=video_name))

        file_ = open('{}'.format(file_name), 'w')
        file_.write('Start at : {sec} \n End at : {sec1} '.format(sec=start, sec1=end))
        file_.close()

    def send_frame_signal(self, frame_range):

        # frame range is like [(0,21),(4,198)]

        assert type(frame_range) is list, "Frame range must have to be a list"

        fps = round(self.fps)

        # build video file path name

        ax = str(datetime.datetime.now())
        tm = ax[0:10] + '_' + ax[11:]

        file_n_ = str(self.output_folder + '/' + str(tm))

        os.makedirs(file_n_)

        video_type = os.path.splitext(os.path.basename(str(self.file_name)))[1]  # output e.g as .mp4

        for ux in range(len(frame_range)):
            start = core_overwatch.time_cut(self, input_in_sec=math.ceil(frame_range[ux][0] / fps))
            end = core_overwatch.time_cut(self, input_in_sec=math.ceil(frame_range[ux][1] / fps))
            end1 = core_overwatch.time_cut(self, input_in_sec=math.ceil(
                (frame_range[ux][1] / fps) - (frame_range[ux][0] / fps)))

            print('[++++++]Start at {0} End at {1}'.format(start, end))

            core_overwatch.build_output(self, start=str(start),
                                        end=str(end),
                                        video_name=file_n_ + '/output{vid_number}{type_v}'.format(vid_number=ux,
                                                                                                  type_v=video_type),
                                        file_name=file_n_ + '/output{0}.txt'.format(ux),
                                        end1=end1
                                        )

        print("Total {0} Videos have been cut from Main Video".format(len(os.listdir(file_n_))/2))


if __name__ == "__main__":
    a = core_overwatch(file_name=str(args['file']), output_folder=str(args['output']), before=int(args['before']),
                       after=int(args['after']))

    a.build_folder()

    start_frame, n, common_diff = a.which_frame_formula()  # returns a,n,d
    c = a.select_frame(start_frame, n, common_diff)  # returns which_frame_list

    st = time.time()
    print("[+++++]Reading Frames....")
    a.read_save_frame()
    print("[+++++++]Finished Reading Frames")

    print("[+++++++]Image Processing Rolling....")
    d = a.get_action_process_multithreaded_cmd_run_commands()
    print("[++++++++]Finished Processing Images")

    f = a.action_index_find(raw_list=d, which_frame=c)  # return list to start aft and bef(action first observed)
    g = a.build_frame_range_to_cut(f)

    a.send_frame_signal(frame_range=g)

    print('[++++++]Time req to run The Engine is {0}m'.format((time.time() - st) / 60))

    print('Deleting temp folders..')
    shutil.rmtree('./raw_calc/frame_db_temp')
    os.remove('./tmp1')
    os.remove('./tmp2')
