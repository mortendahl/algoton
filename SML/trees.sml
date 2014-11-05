datatype 'a tree =
    Leaf of 'a
    | Branch of 'a * 'a tree * 'a tree
    
fun size(Leaf(_)) = 0
  | size(Branch(_, left, right)) = 1 + size(left) + size(right)
  
fun depth(Leaf(_)) = 0
  | depth(Branch(_, left, right)) = 1 + Int.max( depth(left), depth(right) ) 
  
fun gentree(0, k) = Leaf(k)
  | gentree(depth, k) = Branch(k, gentree(depth-1, 2*k), gentree(depth-1, 2*k+1))

fun gensametree(0, s) = Leaf(s)
  | gensametree(depth, s) =
        let val leftright = gensametree(depth-1, s)
        in Branch(s, leftright, leftright) end
            
fun gensametree'(0, s, leftright) = leftright
  | gensametree'(depth, s, leftright) = gensametree'(depth-1, s, Branch(s, leftright, leftright))
        
fun reflect(t as Leaf(_)) = t
  | reflect(Branch(s, left, right)) = Branch(s, right, left)
