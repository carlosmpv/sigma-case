'use client'
import type { FeatureCollection, GeoJsonProperties, Geometry } from 'geojson'
import type { Product } from "../actions/products"
import type { SoilUsage } from '../actions/map'
import Products from './products'
import SoilList from "./soil_usage";
import MapComponent from './map'
import { useState } from 'react'

export default function Dashboard(
  state: {
    products: Product[],
    mapPolygons: FeatureCollection<Geometry, GeoJsonProperties> | null,
    soilUsage: SoilUsage[]
  }
) {
  const [selectedSoil, selectSoil] = useState<SoilUsage | null>(null)

  return <div className="flex">
      <aside className="w-screen lg:w-96 border-r border-gray-300 h-screen overflow-y-scroll">
        <Products products={state.products} />
        <SoilList soils={state.soilUsage} onSoilSelect={selectSoil} />
      </aside>
      <main className="flex-1 h-screen overflow-hidden">
        <MapComponent polygons={state.mapPolygons!} selectedSoil={selectedSoil}/>
      </main>
    </div>
}