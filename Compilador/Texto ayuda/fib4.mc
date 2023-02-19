/*
fib.mc

calcula el n-esimo número de la secuencia de Fibonacci
*/

fun fib(n){
  if (n <= 1){
    return 1;
  }else{
    return fib(n-1) + fib(n-2);
  }
  end_if
}

for(var i = 0; i < 21; i += 1){
  print(fib(i));
}
