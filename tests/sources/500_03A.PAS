{
@name: Kozlov Ilya
@task: A
}
program A;
var f1,f2:text;
    h,i,k,v,p:integer;
    l:array[1..1000] of integer;
    j:array[1..1000] of integer;
 begin
  assign(f1,'imput.txt');
  assign(f2,'output.txt');
  reset(f1);
  read(f1,h);
  for i:=1 to h do begin
  read(f1,k);
  l[i]:=k;
  read(f1,k);
  j[i]:=k;
  end;
  v:=0;
  for i:=1 to h do
   for p:=i+1 to h do
    if l[i]>l[p] then begin
       v:=l[p];
       l[p]:=l[i];
       l[i]:=v;
       v:=j[p];
       j[p]:=j[i];
       j[i]:=v;
                       end
                 else if l[i]=l[p] then
                  if j[i]>j[p] then begin
                   v:=j[p];
                   j[p]:=j[i];
                   j[i]:=v;
                   end;
  rewrite(f2);
  for i:=1 to h do writeln(f2,l[i],' ',j[i]);
  close(f2);
  close(f1);
  readln;
  end.