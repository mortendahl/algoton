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
  | ((x::xs) subset ys) = (x mem ys) andalso (xs subset ys);
  
infix seteq;
fun (xs seteq ys) = (xs subset ys) andalso (ys subset xs);
  
fun powerset([], base)     = [base]
  | powerset(x::xs, base)  = powerset(xs, base) @ powerset(xs, x::base);

fun carprod([], ys)       = []
  | carprod(x::xs, ys)    =
        let fun pairx([])       = carprod(xs, ys)
              | pairx(y::ys)    = (x,y) :: pairx(ys)
        in
        pairx(ys)
        end;

(* note that, compared to carprod above, this version does not waits until the 
   very end to concatenate elements, meaning it uses a smaller recursion stack *)
fun carprod'([], ys)       = []
  | carprod'(x::xs, ys)    =
        let val xsprod          = carprod'(xs, ys)
            fun pairx([])       = xsprod
              | pairx(y::ys)    = (x,y) :: pairx(ys)
        in
        pairx(ys)
        end;

fun len([]) = 0
  | len(x::xs) = 1 + len(xs);

fun prefix(x, []) = []
  | prefix(x, y::ys) = (x::y) :: prefix(x, ys);

fun kcombs(0, xs) = [ [] ]
  | kcombs(k, []) = []
  | kcombs(k, x::xs) = 
        let val l = len(x::xs) 
        in
            if k < l then 
                let fun prefixx([]) = []
                      | prefixx(y::ys) = (x::y) :: prefixx(ys)
                in 
                    kcombs(k, xs) @ prefixx(kcombs(k-1, xs))
                end
            else if k = l then [x::xs]
            else (* if k > l *) []
        end;

(* same optimisation as for carprod' *)
fun kcombs'(0, xs) = [ [] ]
  | kcombs'(k, []) = []
  | kcombs'(k, x::xs) = 
        let val l = len(x::xs) 
        in
            if k < l then 
                let val exclusive = kcombs'(k, xs)
                    val inclusive = kcombs'(k-1, xs)
                    fun prefixx([]) = exclusive
                      | prefixx(y::ys) = (x::y) :: prefixx(ys)
                in 
                    prefixx(inclusive)
                end
            else if k = l then [x::xs]
            else (* if k > l *) []
        end;