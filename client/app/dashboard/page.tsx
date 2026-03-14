
import { getGeoJSON } from "../actions/map";
import { getProducts } from "../actions/products"
import MapComponent from "../ui/maps";
import Products from "../ui/products";

export default async function StockPage() {
  const products = await getProducts();
  const mapPolygons = await getGeoJSON();

  return <div className="flex">
    <aside className="w-screen lg:w-96 p-4 border-r border-gray-300 h-screen overflow-y-scroll">
      <Products products={products} />
    </aside>
    <main className="flex-1 h-screen overflow-hidden">
      <MapComponent polygons={mapPolygons!}/>
    </main>
  </div>
}