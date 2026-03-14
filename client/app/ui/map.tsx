'use client'
import type { FeatureCollection } from 'geojson'
import { Map, type GeoJSONSource } from 'maplibre-gl'
import { useEffect, useRef } from 'react'
import type { SoilUsage } from '../actions/map'

export default function MapComponent(
  state: {
    polygons?: FeatureCollection
    selectedSoil?: SoilUsage | null
  }
) {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<Map | null>(null)
  const previousSelectedId = useRef<string | number | null>(null)

  const applySelection = () => {
    if (!map.current) return
    if (!map.current.getSource('internal-source')) return

    if (previousSelectedId.current != null) {
      map.current.setFeatureState(
        { source: 'internal-source', id: previousSelectedId.current },
        { selected: false }
      )
    }

    if (state.selectedSoil?.id) {
      map.current.setFeatureState(
        { source: 'internal-source', id: state.selectedSoil.id },
        { selected: true }
      )
      previousSelectedId.current = state.selectedSoil.id
    } else {
      previousSelectedId.current = null
    }
  }

  useEffect(() => {
    if (map.current) return
    if (!mapContainer.current) return

    const instance = new Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors'
          }
        },
        layers: [
          {
            id: 'osm',
            type: 'raster',
            source: 'osm'
          }
        ]
      },
      center: [-49.550597, -20.482847],
      zoom: 13
    })

    map.current = instance

    instance.on('load', () => {
      if (!state.polygons) return

      instance.addSource('internal-source', {
        type: 'geojson',
        data: state.polygons,
        promoteId: 'uuid'
      })

      instance.addLayer({
        id: 'polygons',
        type: 'fill',
        source: 'internal-source',
        paint: {
          'fill-color': ['get', 'rgb'],
          'fill-opacity': [
            'case',
            ['boolean', ['feature-state', 'selected'], false],
            0.8,
            0.2,
          ]
        }
      })

      applySelection()
    })

    return () => {
      instance.remove()
      map.current = null
    }
  }, [])

  useEffect(() => {
    if (!map.current) return
    const source = map.current.getSource('internal-source') as GeoJSONSource | undefined
    if (!source || !state.polygons) return

    source.setData(state.polygons)
    applySelection()
  }, [state.polygons])

  useEffect(() => {
    applySelection()
  }, [state.selectedSoil])

  return <div ref={mapContainer} className="h-full" />
}