import type { FeatureCollection } from 'geojson'
import { getAccessToken } from "@/utils/token";


export async function getGeoJSON(): Promise<FeatureCollection | null> {
  const token = await getAccessToken()!
  
  const response = await fetch(`${process.env.API_URL}/secured/map/features`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    console.error('Falha ao obter GeoJSON')
    return null
  }
  
  const polygons = await response.json()
  return polygons as FeatureCollection
}