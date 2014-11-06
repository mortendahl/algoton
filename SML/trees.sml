datatype 'a tree =
    Leaf of 'a
    | Branch of 'a * 'a tree * 'a tree
    
fun size(Leaf(_)) = 0
  | size(Branch(_, left, right)) = 1 + size(left) + size(right)
  
fun depth(Leaf(_)) = 0
  | depth(Branch(_, left, right)) = 1 + Int.max( depth(left), depth(right) ) 
  
(*
 * Generate tree of specified depth with values 1 .. 2^{depth+1}-1
 *  - initial call is gentree(depth, 1)
 *)
fun gentree(0, k) = Leaf(k)
  | gentree(depth, k) = Branch(k, gentree(depth-1, 2*k), gentree(depth-1, 2*k+1))

(*
 * Generate tree of specified depth with the same satellite value s in every node
 *)
fun gensametree(0, s) = Leaf(s)
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
fun reflect(t as Leaf(_)) = t
  | reflect(Branch(s, left, right)) = Branch(s, reflect(right), reflect(left))

(*
 * Decide if t1 = reflect(t2)
 *)
fun eqReflect(Leaf(s1), Leaf(s2)) = s1 = s2
  | eqReflect(t1 as Branch(s1,left1,right1), t2 as Branch(s2,left2,right2)) =
        s1 = s2 andalso eqReflect(left1,right2) andalso eqReflect(right1,left2)
  | eqReflect(_, _) = false

(*
 * Naively decide whether tree is balanced
 *)     
fun isBalanced(Leaf(_)) = true
  | isBalanced(Branch(_, left, right)) = isBalanced(left) andalso isBalanced(right) andalso abs(size(left) - size(right)) <= 1

(*
 * Improved by only doing one recursion 
 *)
fun isBalanced'(Leaf(_)) = (true, 0)
  | isBalanced'(Branch(_, left, right)) =
        let val (isBalancedRight, sizeLeft) = isBalanced'(left)
            val (isBalancedLeft, sizeRight) = isBalanced'(right)
            val balanced = isBalancedLeft andalso isBalancedRight andalso abs(sizeLeft - sizeRight) <= 1
            val size = 1 + sizeLeft + sizeRight
        in (balanced, size) end