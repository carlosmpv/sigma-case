
import { getGeoJSON, getSoilUsage } from "../actions/map";
import { getProducts } from "../actions/products"
import MapComponent from "../ui/map";
import Products from "../ui/products";
import SoilUsage from "../ui/soil_usage";

export default async function StockPage() {
  const products = await getProducts();
  const mapPolygons = await getGeoJSON();
  const soilUsage = await getSoilUsage();

  return <div className="flex">
    <aside className="w-screen lg:w-96 border-r border-gray-300 h-screen overflow-y-scroll">
      <Products products={products} />
      <SoilUsage soils={soilUsage} />
    </aside>
    <main className="flex-1 h-screen overflow-hidden">
      <MapComponent polygons={mapPolygons!}/>
    </main>
  </div>
}