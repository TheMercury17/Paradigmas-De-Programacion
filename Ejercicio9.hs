-- Pedido de pizza - Haskell

import Data.Char (toLower)
import Text.Read (readMaybe)
import Data.Maybe (fromMaybe)

vegMenu :: [String]
vegMenu = ["Pimiento", "Champinones", "Aceitunas", "Tomate", "Cebolla"]

nonVegMenu :: [String]
nonVegMenu = ["Pepperoni", "Jamon", "Salchicha", "Bacon", "Anchoas"]

-- descripcionPizza toma:
--   isVeg  -> Bool (True si es vegetariana)
--   extra  -> String (ingrediente adicional elegido)
-- Devuelve (descripcion, esVegetariana)
descripcionPizza :: Bool -> String -> (String, Bool)
descripcionPizza isVeg extra =
  let tipo = if isVeg then "vegetariana" else "no vegetariana"
      base = "masa, salsa de tomate y queso"
      ingrediente = if null extra then "sin ingrediente adicional" else extra
      descripcion = "Pizza " ++ tipo ++ " con " ++ base ++ " y adicional: " ++ ingrediente ++ "."
  in (descripcion, isVeg)

-- Helpers para mostrar menus y leer elección
mostrarMenu :: [String] -> IO ()
mostrarMenu menu = mapM_ putStrLn $ zipWith (\i it -> show i ++ ". " ++ it) [1::Int ..] menu

leerSiNo :: String -> IO (Maybe Bool)
leerSiNo prompt = do
  putStrLn prompt
  r <- getLine
  case map toLower (filter (/= ' ') r) of
    (c:_) | c == 's' || c == 'y' -> return (Just True)
    (c:_) | c == 'n'             -> return (Just False)
    _                            -> return Nothing

elegirIngrediente :: [String] -> IO (Maybe String)
elegirIngrediente menu = do
  mostrarMenu menu
  putStrLn "Elige el número del ingrediente adicional (o escribe el nombre):"
  entrada <- getLine
  case readMaybe entrada :: Maybe Int of
    Just n ->
      if n >= 1 && n <= length menu then return (Just (menu !! (n-1)))
      else return Nothing
    Nothing ->
      let nom = map toLower entrada
          match = filter (\it -> map toLower it == nom) menu
      in return $ if null match then Nothing else Just (head match)

-- Main de ejemplo
main :: IO ()
main = do
  mIsVeg <- leerSiNo "¿Deseas una pizza vegetariana? (s/n)"
  case mIsVeg of
    Nothing -> putStrLn "Entrada inválida. Responde 's' o 'n'."
    Just isVeg -> do
      let menu = if isVeg then vegMenu else nonVegMenu
      putStrLn $ "\nMenú para pizza " ++ (if isVeg then "vegetariana:" else "no vegetariana:")
      mIng <- elegirIngrediente menu
      case mIng of
        Nothing -> putStrLn "Selección inválida de ingrediente. Intenta de nuevo y elige un número o nombre válido."
        Just ing -> do
          let (desc, vegFlag) = descripcionPizza isVeg ing
          putStrLn "\n--- Pedido confirmado ---"
          putStrLn desc
          putStrLn $ "(Vegetariana: " ++ (if vegFlag then "Sí" else "No") ++ ")"
