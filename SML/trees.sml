
structure Tree =
struct
    
    datatype 'a tree =  Leaf
                        | Branch of 'a * 'a tree * 'a tree
    
    fun size(Leaf) = 0
      | size(Branch(_, left, right)) = 1 + size(left) + size(right)
  
    fun depth(Leaf) = 0
      | depth(Branch(_, left, right)) = 1 + Int.max( depth(left), depth(right) ) 
  
    (*
     * Generate tree of specified depth with values 1 .. 2^{depth+1}-1
     *  - initial call is gentree(depth, 1)
     *)
    fun gentree(0, k) = Leaf
      | gentree(depth, k) = Branch(k, gentree(depth-1, 2*k), gentree(depth-1, 2*k+1))

    (*
     * Generate tree of specified depth with the same satellite value s in every node
     *)
    fun gensametree(0, s) = Leaf
      | gensametree(depth, s) =
            let val leftright = gensametree(depth-1, s)
            in Branch(s, leftright, leftright) end
            
    (*
     * Tail recursive version of gensametree
     *)
    fun gensametree'(0, s, leftright) = leftright
      | gensametree'(depth, s, leftright) = gensametree'(depth-1, s, Branch(s, leftright, leftright))
   
    (*
     * Mirror the tree
     *)     
    fun reflect(t as Leaf) = t
      | reflect(Branch(s, left, right)) = Branch(s, reflect(right), reflect(left))

    (*
     * Decide if t1 = reflect(t2)
     *)
    fun eqReflect(Leaf, Leaf) = true
      | eqReflect(t1 as Branch(s1,left1,right1), t2 as Branch(s2,left2,right2)) =
            s1 = s2 andalso eqReflect(left1,right2) andalso eqReflect(right1,left2)
      | eqReflect(_, _) = false

    (*
     * Naively decide whether tree is balanced
     *)     
    fun isBalanced(Leaf) = true
      | isBalanced(Branch(_, left, right)) = isBalanced(left) andalso isBalanced(right) andalso abs(size(left) - size(right)) <= 1

    (*
     * Improved by only doing one recursion 
     *)
    fun isBalanced'(Leaf) = (true, 0)
      | isBalanced'(Branch(_, left, right)) =
            let val (isBalancedRight, sizeLeft) = isBalanced'(left)
                val (isBalancedLeft, sizeRight) = isBalanced'(right)
                val balanced = isBalancedLeft andalso isBalancedRight andalso abs(sizeLeft - sizeRight) <= 1
                val size = 1 + sizeLeft + sizeRight
            in (balanced, size) end
            
end

signature DICTIONARY =
sig
    type key
    type 'a t
    exception E of key
    val empty : 'a t
    val member : 'a t * key -> bool
    val lookup : 'a t * key -> 'a
    val insert : 'a t * key * 'a -> 'a t
    val update : 'a t * key * 'a -> 'a t
end

structure QuickListDict : DICTIONARY =
struct
    type key = int
    type 'a t = (key * 'a) list
    
    exception E of key
    
    val empty = []
    
    fun member([], _) = false
      | member((k',_)::xs, k) =
            if k = k' then true
            else member(xs, k)
            
    fun lookup([], k) = raise E k
      | lookup((k',s')::xs, k) =
            if k = k' then s'
            else lookup(xs, k)
            
    (* note, we do not check whether or key already exists or not, unlike in TreeDict *)
    fun insert(xs, k, s) = (k,s)::xs
    
    (* note, we use that lookup just picks the first pair with a matching key; 
       this means that the size of the dict can differ from the number of keys *)
    fun update(xs, k, s) = (k,s)::xs
    
end

structure UniqueListDict : DICTIONARY =
struct
    type key = int
    type 'a t = (key * 'a) list
    
    exception E of key
    
    val empty = []
    
    fun member([], _) = false
      | member((k',_)::xs, k) =
            if k = k' then true
            else member(xs, k)
            
    fun lookup([], k) = raise E k
      | lookup((k',s')::xs, k) =
            if k = k' then s'
            else lookup(xs, k)
            
    fun insert(xs, k, s) = 
            if member(xs, k) then raise E k
            else (k,s)::xs

    fun update([], k, s) = [(k,s)]
      | update((k',s')::xs, k, s) =
            if k = k' then (k,s)::xs
            else (k',s')::update(xs, k, s)

end

structure TreeDict : DICTIONARY =
struct
    type key = int
    type 'a t = (key * 'a) Tree.tree
    
    exception E of key
    
    val empty = Tree.Leaf
    
    fun member(Tree.Leaf, _) = false
      | member(Tree.Branch((k',s'), left, right), k) =
            if k < k' then member(left, k)
            else if k = k' then true
            else (* k' < k *) member(right, k)
    
    fun lookup(Tree.Leaf, k) = raise E k
      | lookup(Tree.Branch((k',s'), left, right), k) =
            if k < k' then lookup(left, k)
            else if k = k' then s'
            else (* k' < k *) lookup(right, k)
            
    fun insert(Tree.Leaf, k, s) = Tree.Branch( (k,s), Tree.Leaf, Tree.Leaf )
      | insert(Tree.Branch((k',s'), left, right), k, s) =
            if k < k' then Tree.Branch( (k',s'), insert(left,k,s), right )
            else if k = k' then raise E k
            else (* k' < k *) Tree.Branch( (k',s'), left, insert(right,k,s) )
        
    fun update(Tree.Leaf, k, s) = Tree.Branch( (k,s), Tree.Leaf, Tree.Leaf )
      | update(Tree.Branch((k',s'), left, right), k, s) =
            if k < k' then Tree.Branch( (k',s'), update(left,k,s), right )
            else if k = k' then Tree.Branch( (k,s), left, right )
            else (* k' < k *) Tree.Branch( (k',s'), left, update(right,k,s) )
end

(* by keeping a best-candidate we can eliminate all equality tests down the tree in exchange for one at the leaf *)
structure OptimisedTreeDict : DICTIONARY =
struct
    type key = int
    type 'a t = (key * 'a) Tree.tree
    
    exception E of key
    
    val empty = Tree.Leaf

    fun member'(Tree.Leaf, k, (k'',_)) = k = k''
      | member'(Tree.Branch(c' as (k',_), left, right), k, c'') =
            if k < k' then member'(left, k, c'')
            else (* k' <= k *) member'(right, k, c')
    
    fun lookup'(Tree.Leaf, k, (k'',s)) = 
            if k = k'' then s
            else raise E k
      | lookup'(Tree.Branch(c' as (k',s'), left, right), k, c'') =
            if k < k' then lookup'(left, k, c'')
            else (* k' <= k *) lookup'(right, k, c')
    
    fun insert'(Tree.Leaf, k, s, (k'',_)) =
            if k = k'' then raise E k
            else Tree.Branch( (k,s), Tree.Leaf, Tree.Leaf )
      | insert'(Tree.Branch(c' as (k',s'), left, right), k, s, c'') =
            if k < k' then Tree.Branch( c', insert'(left,k,s,c''), right )
            else Tree.Branch( c', left, insert'(right,k,s,c') )
    
    fun member(Tree.Leaf, _) = false
      | member(root as Tree.Branch(c', _, _), k) = member'(root, k, c')
    
    fun lookup(Tree.Leaf, k) = raise E k
      | lookup(root as Tree.Branch(c', left, right), k) = lookup'(root, k, c')
            
    fun insert(Tree.Leaf, k, s) = Tree.Branch( (k,s), Tree.Leaf, Tree.Leaf )
      | insert(root as Tree.Branch(c', _, _), k, s) = insert'(root, k, s, c')
        
    (* this one is the naive double-check version; can't see how to do this without an extra
       checking on the way up from the recursive (say, using an optional type), meaning we're
       doing a double-check anyway (plus insisting of always going to the leaf) *)
    fun update(Tree.Leaf, k, s) = Tree.Branch( (k,s), Tree.Leaf, Tree.Leaf )
      | update(Tree.Branch((k',s'), left, right), k, s) =
            if k < k' then Tree.Branch( (k',s'), update(left,k,s), right )
            else if k = k' then Tree.Branch( (k,s), left, right )
            else (* k' < k *) Tree.Branch( (k',s'), left, update(right,k,s) )
    
end

signature HEAP =
sig
    type item
    type t
    val empty : t
    val isEmpty : t -> bool
    val min : t -> item
    val removeMin : t -> t
    val insert : item * t -> t
    val fromList : item list -> t
    val toList : t -> item list
    val sort : item list -> item list
end

structure TreeHeap : HEAP =
struct
    type item = int
    type t = item Tree.tree
    
    val empty = Tree.Leaf
    
    fun isEmpty(Tree.Leaf) = true
      | isEmpty(_) = false

    fun min(Tree.Branch(v, _, _)) = v
    
    fun leftRemove(Tree.Branch(v, Tree.Leaf, Tree.Leaf)) = (v, Tree.Leaf)
      | leftRemove(Tree.Branch(v, left, right)) =
            let val (w, left') = leftRemove(left)
            in (w, Tree.Branch(v, right, left')) end
    
    fun shiftDown(v, left as Tree.Leaf, right as Tree.Leaf) = Tree.Branch(v, left, right)
      | shiftDown(v, left as Tree.Branch(w, Tree.Leaf, Tree.Leaf), right as Tree.Leaf) =
            if v <= w then Tree.Branch(v, left, right)
            else Tree.Branch(w, Tree.Branch(v, Tree.Leaf, Tree.Leaf), Tree.Leaf)
      | shiftDown(v, left as Tree.Branch(leftw, leftleft, leftright), right as Tree.Branch(rightw, rightleft, rightright)) =
            if v <= leftw andalso v <= rightw then Tree.Branch(v, left, right)
            else if leftw <= rightw then Tree.Branch(leftw, shiftDown(v, leftleft, leftright), right)
            else Tree.Branch(rightw, left, shiftDown(v, rightleft, rightright))
    
    fun removeMin(Tree.Leaf) = raise Size
      | removeMin(Tree.Branch(v, Tree.Leaf, _)) = Tree.Leaf
      | removeMin(Tree.Branch(_, left, right)) =
            let val (w, left') = leftRemove left
            in shiftDown(w, right, left') end
      
    fun insert(v, Tree.Leaf) = Tree.Branch(v, Tree.Leaf, Tree.Leaf)
      | insert(v, Tree.Branch(w, left, right)) =
            if v <= w then Tree.Branch(v, insert(w, right), left)
            else Tree.Branch(w, insert(v, right), left)
            
    fun heapify(0, vs) = (Tree.Leaf, vs)
      | heapify(n, v::vs) =
            let val (left, vs') = heapify(n div 2, vs)
                val (right, vs'') = heapify((n-1) div 2, vs')
            in (shiftDown(v, left, right), vs'') end
            
    fun fromList(vs) = #1 (heapify(List.length vs, vs))
    
    fun toList(Tree.Leaf) = []
      | toList(t as Tree.Branch(v, _, _)) = v :: toList(removeMin(t))
    
    fun sort(vs) = toList(fromList(vs))
    
end
    

    