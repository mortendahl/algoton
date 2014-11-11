
(* 
 * classical insertion sort 
 *)
fun insertionsort([]) = []
  | insertionsort(x::xs) = 
        let fun insert([]) = [x]
              | insert(y::ys) =
                    if y < x then y::insert(ys)
                    else x::(y::ys)
        in
        insert(insertionsort(xs))
        end


(*
 * Hoare's quicksort
 *)
fun quicksort([]) = []
  | quicksort(pivot::xs) =
        let fun partition([], left, right) = 
                    (* partitioning done, recurse down both branches *)
                    quicksort(left) @ pivot::quicksort(right)
              | partition(y::ys, left, right) =
                    (* keep partitioning *)
                    if y < pivot then partition(ys, y::left, right)
                    else partition(ys, left, y::right)
        in
        partition(xs, [], [])
        end

(*
 * ... and slightly shorter
 *)
fun quicksort'([]) = []
  | quicksort'(pivot::xs) =
        let val (left, right) = List.partition (fn x => x < pivot) xs
        in (quicksort' left) @ [pivot] @ (quicksort' right) end

(*
 * ... and using accumulator to get rid of append operation 
 *  - initial call is quicksort'(xs, [])
 *)
fun quicksort''([], sorted) = sorted
  | quicksort''(pivot::xs, sorted) =
        let fun partition([], left, right) = 
                    (* partitioning done, recurse down right followed by left *)
                    quicksort''(left, pivot::quicksort''(right, sorted))
              | partition(y::ys, left, right) =
                    (* keep partitioning *)
                    if y < pivot then partition(ys, y::left, right)
                    else partition(ys, left, y::right)
        in
        partition(xs, [], [])
        end
        
        
(*
 * Hoare's (lesser known) quickselect for picking out the element with rank i
 *  - note that average case running time is O(n) since we only ever follow one branch down (compared to O(n logn) of naive sort-then-select)
 *)
fun quickselect(0, [x]) = x
  | quickselect(i, pivot::xs) =
        let fun partition([], lenleft, left, right) =
                    (* partitioning done, meaning we can finally decide down which branch we want to look next *)
                    if i < lenleft then quickselect(i, left)
                    else if i = lenleft then pivot
                    else quickselect(i-lenleft-1, right)
              | partition(y::ys, lenleft, left, right) =
                    (* keep partitioning *)
                    if y < pivot then partition(ys, lenleft+1, y::left, right)
                    else partition(ys, lenleft, left, y::right)
        in
        partition(xs, 0, [], [])
        end


(*
 * Merge two lists, used by Mergesort and O'Keefe's optimisation
 *  - if the two input lists are in sorted order then so is the combined output list
 *)
fun merge([], ys) = ys
  | merge(xs, []) = xs
  | merge(x::xs, y::ys) =
        if x <= y then x::merge(xs, y::ys)
        else y::merge(x::xs, ys)


(*
 * Mergesort (inefficient due to repeated scanning)
 *)        
fun mergesort([]) = []
  | mergesort([x]) = [x]
  | mergesort(xs) =
        let val k = length xs div 2
            val left = List.take(xs,k)
            val right = List.drop(xs,k)
        in 
        merge( mergesort(left), mergesort(right) )
        end


(*
 * Helper functions for O'Keefe's algorithms below
 *)
fun mergepairs([l], k) = [l]
  | mergepairs(l1::l2::ls, k) =
        if k mod 2 = 1 then l1::l2::ls  (* not ready to merge yet *)
        else mergepairs(merge(l1,l2)::ls, k div 2)  (* ready to merge, recursively *)

fun nextrun(run, []) = (List.rev run, [])
  | nextrun(run, x::xs) =
        if List.hd run > x then (List.rev run, x::xs)  (* not in order anymore so can't keep adding to the current run *)
        else nextrun(x::run, xs)  (* in order so keep adding *)

(*
 * O'Keefe's trick for bottom-up mergesort, taking one element at a time
 *  - worst case O(n log n)
 *  - only scans the input once
 *  - initial call is okeffesort(xs, [[]], 0)
 *)
fun okeffesort([], ls, k) = List.hd(mergepairs(ls, 0))
  | okeffesort(x::xs, ls, k) = okeffesort(xs, mergepairs([x]::ls, k+1), k+1)

(*
 * Improved O'Keefe's algorithm, taking a 'run' (i.e. already sorted sublist) at a time
 *  - best case O(n), if already completely sorted
 *  - initial call is okeffesamsort(xs, [[]], 0)
 *)
fun okeffesamsort([], ls, k) = List.hd(mergepairs(ls, 0))
  | okeffesamsort(x::xs, ls, k) =
        let val (run, tail) = nextrun([x], xs)
        in
        okeffesamsort(tail, mergepairs(run::ls, k+1), k+1)
        end
