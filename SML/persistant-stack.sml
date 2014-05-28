


signature Stack =
sig
	type 'a Stack
	
	val empty: 'a Stack     (* empty stack *)
	val isEmpty: 'a Stack -> bool
	val cons: 'a * 'a Stack -> 'a Stack
	val head: 'a Stack -> 'a
	val tail: 'a Stack -> 'a Stack
	val length: 'a Stack -> int
	
	val append: 'a Stack -> 'a Stack -> 'a Stack
	val update: int -> 'a -> 'a Stack -> 'a Stack
	val affixes: 'a Stack -> 'a Stack list
end





(*
structure ListStack: Stack =
struct
    type 'a Stack = 'a list
    
    val empty = []
    fun isEmpty s = null s
    fun cons (x, s) = x :: s
    fun head s = hd s
    fun tail s = tl s
end
*)




structure CustomStack: Stack =
struct
	datatype 'a Stack = 
		Nil
		| Cons of 'a * 'a Stack
	
	val empty = Nil
	
	fun isEmpty Nil = true
		| isEmpty _ = false
		
	fun cons (x, s) = Cons(x, s)
	
	fun head Nil = raise Empty
		| head (Cons(x, s)) = x
		
	fun tail Nil = raise Empty
	    | tail (Cons(x, s)) = s
	    
	fun length Nil = 0
	    | length (Cons(_, s)) = 1 + length s
	    
	fun append Nil s2 = s2
	    | append s1 s2 = Cons(head s1, append (tail s1) s2)
	
	fun update i v Nil = raise Empty
	    | update 0 v s = Cons(v, tail s)
	    | update i v s = Cons(head s, update (i-1) v (tail s))
	    
	fun affixes Nil = [Nil]
	    | affixes (s as Cons(_, s')) = s :: affixes s'
end


val s1 = CustomStack.cons(1, CustomStack.cons(2, CustomStack.cons(3, CustomStack.empty)));;
val s2 = CustomStack.cons(4, CustomStack.cons(5, CustomStack.cons(6, CustomStack.empty)));;    

map (fn s => CustomStack.length s) (CustomStack.affixes s1)

