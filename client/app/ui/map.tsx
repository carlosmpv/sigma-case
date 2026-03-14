'use client'
import type { FeatureCollection } from 'geojson'
import { Map, NavigationControl } from "maplibre-gl"
import { useEffect, useRef, useState } from "react";


type MapState = {
  polygons?: FeatureCollection
};

export default function MapComponent(initialState: MapState) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<Map>(null);


  useEffect(() => {
    if (map.current) return;
    if (!mapContainer.current) return;

    map.current = new Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: [
              "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            ],
            tileSize: 256,
            attribution: "© OpenStreetMap contributors"
          }
        },
        layers: [
          {
            id: "osm",
            type: "raster",
            source: "osm"
          }
        ]
      },
      center: [-49.550597, -20.482847],
      zoom: 13
    })

    map.current.on('load', () => {
      map.current?.addSource('internal-source', {
        type: 'geojson',
        data: initialState.polygons!
      })

      map.current?.addLayer({
        id: 'polygons',
        type: 'fill',
        source: 'internal-source',
        paint: {
          'fill-color': ['get', 'rgb'],
          'fill-opacity': 0.8
        }
      })
    })

    return (() => {
      if (map.current) {
        map.current.remove()
      }
    })
  }, [initialState.polygons])

  return <div ref={mapContainer} className="h-full"></div>
}