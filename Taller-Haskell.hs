--      TALLER DE HASKELL: Resolviendo un problema de negocio
--                  Andres Sebastián Coral Vallejo
--                       ._________________.
--                      |.---------------.|
--                      ||    A.S.C.V.   ||
--                      ||   -._ .-.     ||
--                      ||   -._| | |    ||
--                      ||   -._|"|"|    ||
--                      ||    MERCURY    ||
--                      ||_______________||
--                      /.-.-.-.-.-.-.-.-.\
--                     /.-.-.-.-.-.-.-.-.-.\
--                    /.-.-.-.-.-.-.-.-.-.-.\
--                   /______/__________\___o_\
--                   \_______________________/


import System.Info (os)
import System.Process (callCommand)
import System.IO (hFlush, stdout)
import Data.Char (toLower)

-- Función para limpiar la pantalla
clearScreen :: IO ()
clearScreen = case os of
    "mingw32" -> callCommand "cls"    -- Windows
    _         -> callCommand "clear"  -- Linux / Mac

-- ==============================
-- Gestión de Inventario en Haskell
-- ==============================

type Inventory = [(String, Double, Int)]

-- Normalizar nombres para ignorar mayúsculas/minúsculas
normalize :: String -> String
normalize = map toLower

-- Funciones de inventario -----------------------------

addProduct :: Inventory -> String -> Double -> Int -> Inventory -- Añade un producto
addProduct inventory name price quantity = inventory ++ [(name, price, quantity)]

updateQuantity :: Inventory -> String -> Int -> Inventory -- Actualiza la cantidad
updateQuantity [] _ _ = []
updateQuantity ((n, p, q):xs) name newQuantity
    | normalize n == normalize name = (n, p, newQuantity) : xs
    | otherwise = (n, p, q) : updateQuantity xs name newQuantity

removeProduct :: Inventory -> String -> Inventory -- Remueve un producto
removeProduct inventory name =
    filter (\(n, _, _) -> normalize n /= normalize name) inventory

inventorySummary :: Inventory -> (Int, Double) -- Resume el inventario
inventorySummary inventory = (totalQuantity, totalValue)
  where
    totalQuantity = sum [q | (_, _, q) <- inventory]
    totalValue = sum [p * fromIntegral q | (_, p, q) <- inventory]

findProduct :: Inventory -> String -> Maybe (Double, Int) -- Encuenta un producto
findProduct [] _ = Nothing
findProduct ((n, p, q):xs) name
    | normalize n == normalize name = Just (p, q)
    | otherwise = findProduct xs name

applyDiscount :: Inventory -> Double -> Inventory -- Aplica un descuento general
applyDiscount inventory percent =
    [(n, p * (1 - percent / 100), q) | (n, p, q) <- inventory]

applyDiscountToProduct :: Inventory -> String -> Double -> Inventory -- Aplica un descuneto a un producto
applyDiscountToProduct [] _ _ = []
applyDiscountToProduct ((n, p, q):xs) name percent
    | normalize n == normalize name = (n, p * (1 - percent / 100), q) : xs
    | otherwise = (n, p, q) : applyDiscountToProduct xs name percent

printInventory :: Inventory -> IO () -- Muestra el inventario
printInventory [] = putStrLn "El inventario está vacío."
printInventory inventory = mapM_ printItem inventory
  where
    printItem (n, p, q) =
        putStrLn $ "Producto: " ++ n ++
                   " | Precio: $" ++ show p ++
                   " | Cantidad: " ++ show q

-- ==============================
-- Programa Principal
-- ==============================

main :: IO ()
main = do
    let inventory = [("Manzanas", 0.5, 100), ("Platanos", 0.3, 150), ("Peras", 0.7, 80)] -- Le metí algunos productos desde el principio
    menu inventory

menu :: Inventory -> IO ()
menu inventory = do
    clearScreen
    putStrLn "\n=== MENU DE INVENTARIO ==="
    putStrLn "1. Agregar producto"
    putStrLn "2. Actualizar cantidad"
    putStrLn "3. Eliminar producto"
    putStrLn "4. Mostrar resumen"
    putStrLn "5. Buscar producto"
    putStrLn "6. Aplicar descuento a todos"
    putStrLn "7. Mostrar inventario completo"
    putStrLn "8. Aplicar descuento a un producto"
    putStrLn "0. Salir"
    putStr "Seleccione una opcion: "
    hFlush stdout
    option <- getLine
    case option of
        "1" -> do
            putStr "Nombre del producto: "
            hFlush stdout
            name <- getLine
            putStr "Precio: $"
            hFlush stdout
            price <- readLn
            putStr "Cantidad: "
            hFlush stdout
            qty <- readLn
            menu (addProduct inventory name price qty)

        "2" -> do
            putStr "Nombre del producto: "
            hFlush stdout
            name <- getLine
            putStr "Nueva cantidad: "
            hFlush stdout
            qty <- readLn
            menu (updateQuantity inventory name qty)

        "3" -> do
            putStr "Nombre del producto a eliminar: "
            hFlush stdout
            name <- getLine
            menu (removeProduct inventory name)

        "4" -> do
            let (totalQty, totalValue) = inventorySummary inventory
            putStrLn $ "Total de productos en stock: " ++ show totalQty
            putStrLn $ "Valor total del inventario: $" ++ show totalValue
            _ <- getLine
            menu inventory

        "5" -> do
            putStr "Nombre del producto a buscar: "
            hFlush stdout
            name <- getLine
            case findProduct inventory name of
                Just (p, q) -> putStrLn $ "Precio: $" ++ show p ++ " | Cantidad: " ++ show q
                Nothing -> putStrLn "Producto no encontrado."
            _ <- getLine
            menu inventory

        "6" -> do
            putStr "Porcentaje de descuento: "
            hFlush stdout
            percent <- readLn
            menu (applyDiscount inventory percent)

        "7" -> do
            putStrLn "\n=== Inventario Actual ==="
            printInventory inventory
            _ <- getLine
            menu inventory

        "8" -> do
            putStr "Nombre del producto: "
            hFlush stdout
            name <- getLine
            putStr "Porcentaje de descuento: "
            hFlush stdout
            percent <- readLn
            menu (applyDiscountToProduct inventory name percent)

        "0" -> putStrLn "Saliendo del sistema..."
        _   -> do
            putStrLn "Opcion invalida."
            _ <- getLine
            menu inventory
