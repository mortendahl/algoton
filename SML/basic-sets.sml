fun concat([], ys)    = ys
  | concat(x::xs, ys) = x :: concat(xs, ys);
  
infix mem;
fun (x mem [])      = false
  | (x mem (y::ys)) = (x=y) orelse (x mem ys);
  
fun addunique(x, xs) = if x mem xs then xs else x::xs;

fun union([], ys) = ys
  | union(x::xs, ys) = addunique(x, union(xs, ys));

fun union'([], ys) = ys
  | union'(x::xs, ys) = union'(xs, addunique(x, ys));
  
fun intersect([], ys) = []
  | intersect(x::xs, ys) = if x mem ys then x :: intersect(xs, ys) 
                                       else intersect(xs, ys);
                                       
fun intersect'([], ys, zs) = zs
  | intersect'(x::xs, ys, zs) = if x mem ys then intersect'(xs, ys, x::zs)
                                            else intersect'(xs, ys, zs);

infix subset;
fun ([] subset ys) = true
  | (x::xs subset ys) = (x mem ys) andalso (xs subset ys);
  
infix seteq;
fun (xs seteq ys) = (xs subset ys) andalso (ys subset xs);
  
fun powerset([], base)     = [base]
  | powerset(x::xs, base)  = powerset(xs, base) @ powerset(xs, x::base);

fun cardprod([], ys)       = []
  | cardprod(x::xs, ys)    =
        let fun pairx([])       = cardprod(xs, ys)
              | pairx(y::ys)    = (x,y) :: pairx(ys)
        in
        pairx(ys)
        end;

(* note that, compared to cardprod above, this version does not waits until the 
   very end to concatenate elements, meaning it uses a smaller recursion stack *)
fun cardprod'([], ys)       = []
  | cardprod'(x::xs, ys)    =
        let val xsprod          = cardprod'(xs, ys)
            fun pairx([])       = xsprod
              | pairx(y::ys)    = (x,y) :: pairx(ys)
        in
        pairx(ys)
        end;
        