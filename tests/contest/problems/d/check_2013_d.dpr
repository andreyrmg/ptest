program check_2013_d;

{$APPTYPE CONSOLE}

uses
  SysUtils, CheckerLib;

var
  a, b, c, d: Integer;
begin
  a := Ansf.ReadInteger;
  b := Outf.ReadInteger;
  if a <> b then
      Quit(REC_CHECK_REJECTED, Format('wrong number of victorious team'#13#10 +
          'expected: %d'#13#10 + 
          '  output: %d',
          [a, b]));
  a := Ansf.ReadInteger;
  c := Outf.ReadInteger;
  if a <> c then
      Quit(REC_CHECK_REJECTED, Format('wrong largest number of moves'#13#10 +
          'expected: %d'#13#10 + 
          '  output: %d',
          [a, c]));
  a := Ansf.ReadInteger;
  d := Outf.ReadInteger;
  if a <> d then
      Quit(REC_CHECK_REJECTED, Format('wrong largest number of moves'#13#10 +
          'expected: %d'#13#10 + 
          '  output: %d',
          [a, d]));
  Quit(REC_CHECK_ACCEPTED, 'Ok: ' + IntToStr(b) + ' ' + IntToStr(c) + ' ' + IntToStr(d));
end.
