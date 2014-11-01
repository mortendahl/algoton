fun neighbours([], v) = []
  | neighbours((w,w')::es, v) =
        if v=w then w'::neighbours(es, v)
        else neighbours(es, v)

infix mem
fun (x mem []) = false
  | (x mem (y::ys)) = (x=y) orelse (x mem ys)
        
fun dfs(graph, [], visited) = visited
  | dfs(graph, v::vs, visited) =
        if v mem visited then dfs(graph, vs, visited)
        else dfs(graph, neighbours(graph, v) @ vs, v::visited)

fun dfs'(graph, [], visited) = visited
  | dfs'(graph, v::vs, visited) =
        dfs'(graph, vs, if v mem visited then visited
                        else dfs'(graph, neighbours(graph,v), v::visited))

fun newvisit(v, (visited,cycles)) = (v::visited, cycles)

fun toposort(graph, [], path, result) = result
  | toposort(graph, v::vs, path, (visited,cycles)) =
        toposort( graph, vs, path, 
            if v mem path then (visited,(rev (v::path))::cycles)
            else if v mem visited then (visited,cycles)
            else newvisit(v, toposort(graph, neighbours(graph,v), v::path, (visited,cycles))) )