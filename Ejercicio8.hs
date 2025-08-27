-- Precios de Arcade - Haskell
import Text.Read (readMaybe)

-- Devuelve Either String Double: Left = error, Right = precio
precioBoleto :: Int -> Either String Double
precioBoleto edad
  | edad < 0  = Left "Edad inválida: no puede ser negativa."
  | edad <= 3 = Right 0.0
  | edad <= 12 = Right 5.0
  | edad <= 17 = Right 7.0
  | edad <= 64 = Right 12.0
  | otherwise  = Right 8.0  -- 65+

mostrarPrecio :: Int -> String
mostrarPrecio edad = case precioBoleto edad of
  Left err   -> err
  Right 0.0  -> "Precio: Entrada gratuita."
  Right p    -> "Precio del boleto: $" ++ show p

main :: IO ()
main = do
  putStrLn "Ingresa la edad del cliente:"
  line <- getLine
  case readMaybe line :: Maybe Int of
    Just edad -> putStrLn (mostrarPrecio edad)
    Nothing   -> putStrLn "Entrada inválida: por favor ingresa un número entero no negativo."
