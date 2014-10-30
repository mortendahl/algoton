fun concat1([], ys)    = ys
  | concat1(x::xs, ys) = x :: concat1(xs, ys);

fun concat2([], ys)    = ys
  | concat2(x::xs, ys) = concat2(xs, x::ys);
  
infix mem;
fun (x mem [])      = false
  | (x mem (y::ys)) = (x=y) orelse (x mem ys);
  
fun addunique(x, xs) = if x mem xs then xs else x::xs;

fun union([], ys) = ys
  | union(x::xs, ys) = union(xs, addunique(x, ys));
  


fun powerset([], base)     = [base]
  | powerset(x::xs, base)  = powerset(xs, base) @ powerset(xs, x::base);



(* note that, compared to cardprod2 below, this version waits until the very 
   end to concatenate elements, meaning it use a much large recursion stack *)
fun cardprod1([], ys)       = []
  | cardprod1(x::xs, ys)    =
        let fun pairx([])       = cardprod1(xs, ys)
              | pairx(y::ys)    = (x,y) :: pairx(ys)
        in
        pairx(ys)
        end;



fun cardprod2([], ys)       = []
  | cardprod2(x::xs, ys)    =
        let val xsprod          = cardprod2(xs, ys)
            fun pairx([])       = xsprod
              | pairx(y::ys)    = (x,y) :: pairx(ys)
        in
        pairx(ys)
        end;
        