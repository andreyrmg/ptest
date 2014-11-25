program check_2013_a;

{$APPTYPE CONSOLE}

uses
  SysUtils, CheckerLib;

var
  n, I: integer;
  a, b: string;
  s: string;
begin
  n := Inf.ReadInteger;
  s := '';
  for I := 1 to n do
  begin
    a := TrimRight(Ansf.ReadString);
    b := TrimRight(Outf.ReadString);
    if a <> b then
      Quit(REC_CHECK_REJECTED, Format(
          'line: %d:'#13#10 +
          'expected: %s'#13#10 + 
          '  output: %s',
          [I, a, b]));
    s := s + a + #13#10;
  end;
  Quit(REC_CHECK_ACCEPTED, 'Ok'#13#10 + s);
end.
