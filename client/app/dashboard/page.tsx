
import { getGeoJSON, getSoilUsage } from "../actions/map";
import { getProducts, getTotal, transactionHistory } from "../actions/products"
import Dashboard from "../ui/dashboard";

export default async function DashboardPage() {
  const products = await getProducts();
  const mapPolygons = await getGeoJSON();
  const soilUsage = await getSoilUsage();
  const transactions = await transactionHistory();
  const currentCash = await getTotal();
  
  return <Dashboard 
    initialCashAmount={currentCash}
    products={products}
    mapPolygons={mapPolygons}
    soilUsage={soilUsage}
    initialTransactions={transactions}
  />
}