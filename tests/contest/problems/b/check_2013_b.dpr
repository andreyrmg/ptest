program check_2013_b;

{$APPTYPE CONSOLE}

uses
  SysUtils, CheckerLib;

var
  n, k, I: Integer;
  a, b: Integer;
  s: string;
begin
  n := Inf.ReadInteger;
  k := Inf.ReadInteger;
  s := '';
  for I := 1 to k do
  begin
    a := Ansf.ReadInteger;
    b := Outf.ReadInteger;
    if a <> b then
      Quit(REC_CHECK_REJECTED, Format(
          'number: %d:'#13#10 +
          'expected: %d'#13#10 + 
          '  output: %d',
          [I, a, b]));
    s := s + IntToStr(a) + ' ';
  end;
  Quit(REC_CHECK_ACCEPTED, 'Ok'#13#10 + s);
end.
