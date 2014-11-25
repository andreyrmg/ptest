{
@name: Pavel Katskov
@task: A
}
Program z1;
type Elem=record
          x:LongInt; n:byte;
          s:string[33];
          end;
     TMass=array[1..1000] of Elem;
var M:TMass; N,I,Z:Word; j:byte; errcode:integer; El:Elem;
    s:boolean;
Function power(x,a:byte):longint;
 var i:byte; res:longint;
 begin
  res:=1;
  if a<>0 then for i:=1 to a do res:=res*x;
  power:=res;
 end;
Function Translate(X:String; n:byte):LongInt;
var res:LongInt; s:string[33]; i,c:byte; r:word;
 begin
 if N<=10 then
 begin
       c:=Length(X);
       res:=0;
       For i:=1 to Length(X) do
       begin
             Val(X[i],R,ErrCode);
             Res:=Res+R*Power(N,C-i);
       end;
 end
 else
 begin
  C:=Length(X);
  Res:=0;
  For i:=1 to Length(X) do
  begin
   if (X[i]<'9') and (X[i]>'0') then
   Val(X[i],R,ErrCode) else
   R:=11+Ord(X[i])-(Ord('A'));
   if X[i]='F' then R:=15;
   Res:=Res+R*Power(N,C-I);
  end;
 end;
  Translate:=Res;
 end;
Begin
 assign(Input,'input.txt'); reset(input);
 Assign(output,'output.txt'); Rewrite(output);
 ReadLn(N);
 For i:=1 to N do
  begin
  ReadLn(M[i].S);
  j:=Pos(' ',M[i].S);
  Val(Copy(M[i].S,1,J-1),M[i].N,ErrCode);
  M[i].X:=Translate(Copy(M[i].S,J+1,Length(M[i].S)),M[i].N);
  end;
 Z:=N;
 Repeat
 s:=true;
 for i:=1 to z-1 do
  if (m[i].x>m[i+1].x) or
  ((M[i].X=M[i+1].X) and (M[i].N>M[i+1].N)) then
  begin
   s:=false;
   el:=m[i];
   m[i]:=m[i+1];
   m[i+1]:=el;
  end;
  Dec(z);
 Until s;
 For i:=1 to N do WriteLn(M[i].S);
 Close(OutPut);
End.