//@name: Smirnov Ivan
//@task: A
uses
  sysutils;
type tInt=array[1..9]of byte;
function StrToMyInt(v:string):tInt;
var i,j:integer;temp:tInt;
begin
  j:=length(v);
  for i:=9 downto 9-length(v)+1 do
  begin
    Case v[j] of
    {'0'..'9':
    begin
      temp[i]:=ord(v[j])-ord(0);
    end;}
    'A'..'Z':
    begin
      temp[i]:=ord(v[j])-ord('A')+10;
    end
    else
    begin
      temp[i]:=ord(v[j])-ord('0');
    end;
    end;
    dec(j);
  end;
  for j:=9-length(v) downto 1 do
    temp[j]:=0;
  result:=temp;
end;
function Power(a:integer;b:integer):int64;
var temp,i:integer;
begin
  temp:=1;
  For i:=1 to b do
    temp:=temp*a;
  result:=temp;
end;
function MyIntToDec(v:tInt;r:byte):Integer;
var i,temp:integer;
begin
  temp:=0;
  for i:=9 downto 1 do
  begin
    temp:=temp+v[i]*power(r,9-i);
  end;
  result:=temp;
end;
function ToAnotherRoot(v:Integer;r:byte):tInt;
var i:integer;d,m:integer;tv:integer;temp:tInt;
begin
  tv:=v;
  for i:=9 downto 1 do
  begin
    m:=tv mod r;
    temp[i]:=m;
    tv:=tv div r;
  end;
end;
var i,n:integer;s:string;b:boolean;numbers:array of string;rs:array of integer;r,x:integer;int:tint;ints:array of integer;
begin
  reset(input,'input.txt');
  rewrite(output,'output.txt');
  readln(N);
  setlength(numbers,n);
  setlength(ints,n);
  setlength(rs,n);
  for i:=0 to n-1 do
    Readln(numbers[i]);
  for i:=0 to n-1 do
  begin
    x:=pos(' ',numbers[i]);
    r:=strtoint(copy(numbers[i],1,x-1));
    rs[i]:=r;
    delete(numbers[i],1,x);
    int:=strtomyint(numbers[i]);
    ints[i]:=Myinttodec(int,r);
  end;
  b:=true;
  while b=true do
  begin
    b:=false;
    for i:=0 to high(ints)-1 do
    begin
      if (ints[i]=ints[i+1])and(rs[i]>rs[i+1])
      then
      begin
        x:=ints[i];
        ints[i]:=ints[i+1];
        ints[i+1]:=x;
        x:=rs[i];
        rs[i]:=rs[i+1];
        rs[i+1]:=x;
        s:=numbers[i];
        numbers[i]:=numbers[i+1];
        numbers[i+1]:=s;
        b:=true;
      end;
      if ints[i]>ints[i+1]
      then
      begin
        x:=ints[i];
        ints[i]:=ints[i+1];
        ints[i+1]:=x;
        x:=rs[i];
        rs[i]:=rs[i+1];
        rs[i+1]:=x;
        s:=numbers[i];
        numbers[i]:=numbers[i+1];
        numbers[i+1]:=s;
        b:=true;
      end;
    end;
  end;
  for i:=0 to high(numbers) do
    writeln(rs[i],' ',numbers[i]);
  close(input);
  close(output);
end.
