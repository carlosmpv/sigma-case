'use client'
import type { FeatureCollection } from 'geojson'
import { Map, NavigationControl } from "maplibre-gl"
import { useEffect, useRef, useState } from "react";
import { getGeoJSON } from '../actions/map';


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
      style: 'https://demotiles.maplibre.org/style.json',
      center: [-20.480060, -49.550739],
      zoom: 2
    })

    map.current.addControl(new NavigationControl(), 'top-right');
    map.current.on('load', async () => {

      map.current?.addSource('internal-source', {
        type: 'geojson',
        data: initialState.polygons!
      })

      map.current?.addLayer({
        id: 'polygons',
        type: 'fill',
        source: 'internal-source',
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