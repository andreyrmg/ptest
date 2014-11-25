{
@name:Vladimir Lavrov
@task:A
}
{$A+,B-,D+,E+,F-,G-,I+,L+,N-,O-,P-,Q-,R-,S-,T-,V+,X+}
{$M 16384,0,655360}
program qq;
type elem=record
            x:longint;
            sd:string[7];
            ty:integer;
            s:string[7];
         end;
mas=array [1..1000] of elem;
var i,k,y,n,g,q,b,o,l,z:longint;
    code:integer;
    m:mas;
    j:elem;
    f:boolean;
begin
  assign(input,'input.txt');reset(input);
  assign(output,'output.txt');rewrite(output);
  readln(n);
  for i:=1 to n do
  begin
    readln(m[i].s);
    k:=pos(' ',m[i].s);
    val(copy(m[i].s,k+1,4),m[i].x,code);
    m[i].sd:=copy(m[i].s,k+1,4);
    m[i].sd:=m[i].sd+' ';
    y:=pos(' ',m[i].sd);
    y:=y-1;
    val(copy(m[i].s,1,k-1),b,code);
    m[i].ty:=b;
    o:=0;
    f:=false;
    l:=1;
    q:=m[i].x;
    for g:=1 to y do
    begin
      if f=false then
      begin
        o:=q mod 10;
        f:=true;
      end
      else
      o:=o+((q mod 10)*l);
      q:=q div 10;
      l:=l*b;
    end;
  m[i].x:=o;
  end;
  z:=n;
  repeat
  f:=true;
  for i:=1 to z-1 do
  if (m[i].x>m[i+1].x)
  then
  begin
    j:=m[i];
    m[i]:=m[i+1];
    m[i+1]:=j;
    f:=false;
  end
  else if (m[i].ty)>(m[i+1].ty) then
  begin
    j:=m[i];
    m[i]:=m[i+1];
    m[i+1]:=j;
    f:=false;
  end
  until f=true;
  for i:=1 to n do
  writeln(m[i].s);
  close(output);
end.



