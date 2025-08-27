-- Verificador par o impar - Haskell

-- Función pura que devuelve un String
paridad :: Int -> String
paridad n
  | even n    = show n ++ " es par."
  | otherwise = show n ++ " es impar."

-- Ejemplo de main para uso por consola (opcional)
main :: IO ()
main = do
  putStrLn "Ingresa un número entero:"
  linea <- getLine
  case reads linea :: [(Int, String)] of
    [(n, "")] -> putStrLn (paridad n)
    _         -> putStrLn "Entrada inválida: por favor ingresa un número entero."
