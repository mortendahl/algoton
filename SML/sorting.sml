fun insertionsort([]) = []
  | insertionsort(x::xs) = 
        let fun insert([]) = [x]
              | insert(y::ys) =
                    if y < x then y::insert(ys)
                    else x::(y::ys)
        in
        insert(insertionsort(xs))
        end
        
fun quicksort([]) = []
  | quicksort(pivot::xs) =
        let fun partition([], left, right) = quicksort(left) @ pivot::quicksort(right)
              | partition(y::ys, left, right) =
                    if y < pivot then partition(ys, y::left, right)
                    else partition(ys, left, y::right)
        in
        partition(xs, [], [])
        end

(* added accumulator parameter to avoid append operation *)
fun quicksort'([], sorted) = sorted
  | quicksort'(pivot::xs, sorted) =
        let fun partition([], left, right) = quicksort'(left, pivot::quicksort'(right, sorted))
              | partition(y::ys, left, right) =
                    if y < pivot then partition(ys, y::left, right)
                    else partition(ys, left, y::right)
        in
        partition(xs, [], [])
        end
        
fun quickselect(0, [x]) = x
  | quickselect(i, pivot::xs) =
        let fun partition([], lenleft, left, right) =
                    if i < lenleft then quickselect(i, left)
                    else if i = lenleft then pivot
                    else quickselect(i-lenleft-1, right)
              | partition(y::ys, lenleft, left, right) =
                    if y < pivot then partition(ys, lenleft+1, y::left, right)
                    else partition(ys, lenleft, left, y::right)
        in
        partition(xs, 0, [], [])
        end
