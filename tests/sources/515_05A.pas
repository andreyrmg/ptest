{@name: Chekunov
 @school: 32
 @class: 9
 @task: A
}
type tpole=array[1..100,1..100] of integer;
     telem=record
                 i,j:integer;
                 k:integer;
           end;
var k,si,sj,i,j,kol,N,N1,Code:integer;
    f:text;
    pole:tpole;
    ch:char;
    elem:telem;
    s:string;
Function reead(var f:text):string;
var s,Code:integer;
Begin
     read(f,ch);
     if ch<>' '
     then reead:=ch;
End;
Begin
     randomize;
     assign(f,'input.txt');
     reset(f);
     i:=1;
     while not eof(f) do
           begin
                s:=s+reead(f);
           end;
     s:=s+'#';
     val(s[1],N,Code);
     val(s[3],N1,Code);
     for i:=1 to N do
         for j:=1 to N1 do
             pole[i,j]:=0;
     delete(s,1,3);
     val(s[5],elem.i,Code);
     val(s[7],elem.j,Code);
     pole[elem.i,elem.j]:=1;
     delete(s,5,7);
     while s[i]<>'#' do
           begin
                delete(s,i,i+1);
                kol:=random(10);
                While kol<>0 do
                    Begin
                         dec(kol);
                         i:=1+random(n);
                         j:=1+random(n);
                         k:=1+random(9);
                         if pole[i,j]=0
                         then pole[i,j]:=k;
                    end;
           end;
     if (pole[elem.i+1,elem.j]<>0)and(pole[elem.i-1,elem.j]<>0)and
        (pole[elem.i,elem.j+1]<>0)and(pole[elem.i+1,elem.j-1]<>0)
     then begin
               assign(f,'Output.txt');
               rewrite(f);
               writeln(f,'No Solution');
          end;
close(f);
End.