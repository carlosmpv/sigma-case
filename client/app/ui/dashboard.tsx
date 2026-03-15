'use client'
import type { FeatureCollection, GeoJsonProperties, Geometry } from 'geojson'
import { regTransaction, type Product, type Transaction } from "../actions/products"
import type { SoilUsage } from '../actions/map'
import Products from './products'
import SoilList from "./soil_usage";
import MapComponent from './map'
import { useActionState, useEffect, useRef, useState } from 'react'
import { Map, Marker } from 'maplibre-gl'
import Transactions from './transactions'

function TransactionModal(
  state: {
    isOpen: boolean,
    availableProducts: Product[],
    location: { lng: number, lat: number } | null,
    mapObj: Map | null,
    formAction: ((formData: FormData) => void | Promise<void>),
    onClose: () => void
  }
) {
  const dialogRef = useRef<HTMLDialogElement | null>(null)
  const formRef = useRef<HTMLFormElement | null>(null)

  useEffect(() => {
    if (!dialogRef.current) return;

    if (state.isOpen && !dialogRef.current.open)
      dialogRef.current.showModal()
    if (!state.isOpen && dialogRef.current.open)
      dialogRef.current.close()

  }, [state.isOpen])


  return <dialog
    ref={dialogRef}
    className="rounded-lg p-0 w-full max-w-md backdrop:bg-black/40 m-auto"
    onClose={state.onClose}
  >
    {state.availableProducts.length === 0 ? (
      <div className="flex flex-wrap space-y-2 p-2">
        <h1 className="text-2xl text-center">É necessário primeiramente cadastrar um produto no menu à esquerda.</h1>

        <button
          className="bg-gray-100 text-red-700 p-2 m-1 w-full cursor-pointer hover:bg-gray-200"
          type="button"
          onClick={state.onClose}
        >
          Cancelar
        </button>
      </div>
    ) : (
      <div>
        <form
          ref={formRef}
          action={state.formAction}
          className="flex flex-wrap space-y-2 p-2"
        >
          <input type="hidden" name="lat" value={state.location?.lat ?? ""} />
          <input type="hidden" name="lng" value={state.location?.lng ?? ""} />

          <div className="p-1 w-full">
            <label
              htmlFor="product"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Produto
            </label>
            <select
              id="product"
              name="product"
              className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              required
            >
              {state.availableProducts.map(p => (
                <option key={p.uuid} value={p.uuid}>{p.name}</option>
              ))}
            </select>
          </div>

          <div className="p-1 w-full">
            <label
              htmlFor="quantity"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Quantidade
            </label>
            <input
              className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              type="number"
              step="0.01"
              id="quantity"
              name="quantity"
              placeholder="0,00"
              required
            />
          </div>

          <div className="p-1 w-full">
            <label
              htmlFor="transactionType"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Compra/Venda
            </label>
            <select
              id="transactionType"
              name="transactionType"
              className="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-700"
              defaultValue="buy"
            >
              <option value="buy">Compra</option>
              <option value="sell">Venda</option>
            </select>
          </div>

          <button
            className="bg-gray-100 p-2 m-1 w-full cursor-pointer hover:bg-gray-200"
            type="submit"
          >
            Registrar transação neste local
          </button>

          <button
            className="bg-gray-100 text-red-700 p-2 m-1 w-full cursor-pointer hover:bg-gray-200"
            type="button"
            onClick={state.onClose}
          >
            Cancelar
          </button>

        </form>
      </div >
    )
    }
  </dialog >
}

export default function Dashboard(
  state: {
    products: Product[],
    initialTransactions: Transaction[],
    initialCashAmount: number,
    mapPolygons: FeatureCollection<Geometry, GeoJsonProperties> | null,
    soilUsage: SoilUsage[]
  }
) {
  const [selectedSoil, selectSoil] = useState<SoilUsage | null>(null)
  const [isModalOpen, setModalOpen] = useState(false)
  const [products, setProducts] = useState(state.products)
  const [selectedLocation, setSelectedLocation] = useState<{ lng: number, lat: number } | null>(null)
  const [mapInstance, setMapInstance] = useState<Map | null>(null)
  const [transactions, setTransactions] = useActionState(regTransaction, state.initialTransactions)
  const [cash, setCash] = useState(state.initialCashAmount)

  useEffect(() => {
    if (transactions?.length === 0) return
    const total = transactions.reduce((acc, transaction) => {

      const price = transaction.updated_product?.price_per_quantity ?? 0
      return acc + (transaction.quantity * price)
    }, 0)

    setCash(-total)
  }, [transactions])

  function handleMapClick(mapObj: Map, loc: { lng: number, lat: number }) {
    setMapInstance(mapObj)
    setSelectedLocation(loc)
    setModalOpen(true)
  }

  function handleTransactionConfirm(formData: FormData) {
    if (!selectedLocation || !mapInstance) return

    new Marker()
      .setLngLat([selectedLocation.lng, selectedLocation.lat])
      .addTo(mapInstance)

    setTransactions(formData)
    setModalOpen(false)
  }

  function handleModalClose() {
    setModalOpen(false)
    setSelectedLocation(null)
  }

  return <div className="flex">
    <aside className="w-screen lg:w-96 border-r border-gray-300 h-screen overflow-y-scroll">
      <Transactions total={cash} transactions={transactions} />
      <Products products={state.products} onProductsChange={setProducts} />
      <SoilList soils={state.soilUsage} onSoilSelect={selectSoil} />
    </aside>
    <main className="flex-1 h-screen overflow-hidden">
      <MapComponent
        polygons={state.mapPolygons!}
        selectedSoil={selectedSoil}
        onClick={handleMapClick}
      />
      <TransactionModal
        isOpen={isModalOpen}
        availableProducts={products}
        location={selectedLocation}
        mapObj={mapInstance}
        formAction={handleTransactionConfirm}
        onClose={handleModalClose}
      />
    </main>
  </div>
}