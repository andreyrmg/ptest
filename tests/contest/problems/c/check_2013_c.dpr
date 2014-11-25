program check_2013_c;

{$APPTYPE CONSOLE}

uses
  SysUtils, CheckerLib;

var
  a, b: string;
begin
  a := TrimRight(Ansf.ReadString);
  b := TrimRight(Outf.ReadString);
  if a <> b then
      Quit(REC_CHECK_REJECTED, Format(
          'expected: %s'#13#10 + 
          '  output: %s',
          [a, b]));
  Quit(REC_CHECK_ACCEPTED, 'Ok'#13#10 + a);
end.
