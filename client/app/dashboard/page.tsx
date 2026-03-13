
import { getProducts } from "../actions/products"
import Products from "../ui/products";

export default async function StockPage() {
  const products = await getProducts();
  
  return <>
    <aside className="w-screen lg:w-96 p-4 border-r border-gray-300 h-screen overflow-y-scroll">
      <Products products={products}/>
    </aside>
  </>
}