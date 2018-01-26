raw = load 'record.txt' using PigStorage('\t') as (f1:chararray, f2:chararray, f3:chararray, f4:chararray);
ext = FOREACH raw GENERATE REGEX_EXTRACT(f3, 'M(\\d+)R', 1) AS num;
DUMP ext;