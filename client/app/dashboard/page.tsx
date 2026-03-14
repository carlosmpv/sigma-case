
import { getGeoJSON, getSoilUsage } from "../actions/map";
import { getProducts } from "../actions/products"
import Dashboard from "../ui/dashboard";

export default async function DashboardPage() {
  const products = await getProducts();
  const mapPolygons = await getGeoJSON();
  const soilUsage = await getSoilUsage();

  
  return <Dashboard 
    products={products}
    mapPolygons={mapPolygons}
    soilUsage={soilUsage}
  />
}