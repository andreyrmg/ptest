//@name: Oleg Favstov
//@task: A
uses
  SysUtils;
Type rec=record
         sy:integer;
         ch:integer;
         s:string;
         end;
Var n,i:integer;s:string;wsp:rec;
    m:array[0..1001]of rec; f:boolean;
Procedure perevod(Sy:integer;Var ch:integer;s:string);
Var i,j,ot,pr:integer;
Begin
  ot:=0;
  for i:=length(s) downto 1 do
    begin
      if s[i] in ['0'..'9']
      then pr:=ord(s[i])-ord('0')
      else pr:=ord(s[i])-ord('A')+10;
      for j:=1 to (length(s)-i) do
        pr:=pr*sy;
      ot:=ot+pr;
    end;
  ch:=ot;
end;
Procedure qSort(Var m:array of rec;low,high:integer);
Var i,j:integer;a,wsp:rec;
Begin
  i:=low;j:=high;a:=m[(i+j) div 2];
  repeat
    while m[i].ch<a.ch do inc(i);
    while m[j].ch>a.ch do dec(j);
    if i<=j
    then begin
           wsp:=m[i];
           m[i]:=m[j];
           m[j]:=wsp;
           inc(i);
           dec(j);
         end;
  until i>j;
  if i<high then qSort(m,i,high);
  if low<j then qSort(m,low,j);
end;
{Procedure obrper(sy,ch:integer;Var s:string);
Var x:integer;c:char;
Begin
  s:='';
  while ch<>0 do
    begin
      x:=ch mod sy;
      ch:=ch div sy;
      if x>=10
      then c:=chr(ord('A')+x-10)
      else c:=chr(ord('0')+x);
      s:=c+s;
    end;
end;}
Begin
  assign(input,'input.txt');
  assign(output,'output.txt');
  readln(n);
  for i:=1 to n do
    begin
      read(m[i].sy);
      readln(s);
      delete(s,1,1);
      m[i].s:=s;
      perevod(m[i].sy,m[i].ch,s);
    end;
  qSort(m,1,n);
  repeat
    f:=true;
    for i:=1 to n-1 do
      if (m[i].ch=m[i+1].ch)and(m[i].sy>m[i+1].sy)
      then begin
             wsp:=m[i];
             m[i]:=m[i+1];
             m[i+1]:=wsp;
             f:=false;
           end;
  until f;
  for i:=1 to n do
    writeln(m[i].sy,' ',m[i].s);
end.
