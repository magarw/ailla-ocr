import editdistance as ed
import os 

def calculate_metrics(predicted_text, transcript):
    cer = ed.eval(predicted_text, transcript) / float(len(transcript))
    pred_spl = predicted_text.split()
    transcript_spl = transcript.split()
    wer = ed.eval(pred_spl, transcript_spl) / float(len(transcript_spl))
    return cer, wer



total_files = 0
languages = [x  for x in os.listdir("../lang_wise_folders/") if 'DS_Store' not in x ]
for lang in languages:
    print("\nLanguage: ", lang)
    src1 = f"../lang_wise_folders/{lang}/aligned/src1_{lang}/"
    tgt = f"../lang_wise_folders/{lang}/aligned/tgt_{lang}/"

    filenames = [x for x in os.listdir(src1) if '.txt' in x]

    total_cer = 0
    total_wer = 0
    num_lines = 0
    for f in filenames:
        src1_filename = f"{src1}{f}"
        tgt_filename = f"{tgt}{f}"

        src1_lines = open(src1_filename, encoding="utf8").readlines()
        src2_lines = src1_lines
        tgt_lines = open(tgt_filename, encoding="utf8").readlines()

        for src1_line, src2_line, tgt_line in zip(src1_lines, src2_lines, tgt_lines):
            if (not src1_line.strip()) or (not src2_line.strip()) or (not tgt_line.strip()):
                continue
            # cer, _ = calculate_metrics(src1_line.strip(), tgt_line.strip())
            cer, wer = calculate_metrics(
                src1_line.strip().replace('"', "”").replace("'", "’"),
                tgt_line.strip().replace('"', "”").replace("'", "’"),
            )
            total_cer += cer
            total_wer += wer
            num_lines += 1
        total_files += 1


    print("CER:", f"{total_cer * 100 / num_lines :.2f}")
    print("WER:", f"{total_wer * 100 / num_lines :.2f}")
    print("Total files:", total_files)
