
signature Ordered =
sig
    type T
    
    val eq: T -> T -> bool
    val lt: T -> T -> bool
    val gt: T -> T -> bool
    
    val leq: T -> T -> bool
    val geq: T -> T -> bool
end




signature Heap =
sig
    structure Elem: Ordered
    
    type Heap
    
    val empty: Heap
    val isEmpty: Heap -> bool
    
    val insert: Elem.T -> Heap -> Heap
    
    val findMin: Heap -> Elem.T
    val deleteMin: Heap -> Heap
    
    val merge: Heap -> Heap -> Heap
end





functor LeftistHeap (Element: Ordered): Heap =
struct
    
    structure Elem = Element
    
    datatype Heap = 
	    Nil
	    | Node of Elem.T * int * Heap * Heap

    val empty = Nil
    
    fun isEmpty Nil = true
        | isEmpty _ = false
    
    fun distance Nil = 0
        | distance (Node(_, d, _, _)) = d
            
    fun mergeHelper x b1 b2 =
        if distance b1 <= distance b2 then
            Node(x, 1 + distance b1, b2, b1)
        else
            Node(x, 1 + distance b2, b1, b2)
            
    fun merge h Nil = h
        | merge Nil h = h
        | merge (h1 as Node(x1, d1, l1, r1)) (h2 as Node(x2, d2, l2, r2)) =
            if Elem.leq x1 x2 then
                (* keep h1 as root *)
                mergeHelper x1 l1 (merge r1 h2)
            else
                (* keep h2 as root *)
                mergeHelper x2 l2 (merge r2 h1)
        
    fun insert x h =
        merge (Node(x, 1, Nil, Nil)) h
    
    fun findMin Nil = raise Empty
        | findMin (Node(x, _, _, _)) = x
        
    fun deleteMin Nil = raise Empty
        | deleteMin (Node(_, _, l, r)) = merge l r
end
        

    
val h1 = LeftistHeap.insert 3 (LeftistHeap.insert 2 (LeftistHeap.insert 1 (LeftistHeap.insert 0 LeftistHeap.empty)));;
