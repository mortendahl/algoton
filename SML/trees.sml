
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
        
    (* TODO finish this one *)
    fun update(Tree.Leaf, k, s) = Tree.Branch( (k,s), Tree.Leaf, Tree.Leaf )
      | update(Tree.Branch((k',s'), left, right), k, s) =
            if k < k' then Tree.Branch( (k',s'), update(left,k,s), right )
            else if k = k' then Tree.Branch( (k,s), left, right )
            else (* k' < k *) Tree.Branch( (k',s'), left, update(right,k,s) )
    
end

val t0 = OptimisedTreeDict.empty    
val t1 = OptimisedTreeDict.insert(t0, 1, "a")
val t2 = OptimisedTreeDict.insert(t1, 2, "b")
val t3 = OptimisedTreeDict.insert(t2, 3, "c")
    