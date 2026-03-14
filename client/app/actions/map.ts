import type { FeatureCollection } from 'geojson'
import { getAccessToken } from "@/utils/token";
import { redirect } from 'next/navigation';

export type SoilUsage = {
  id: string
  desc_uso_solo: string
  rgb: string
  area: number
}

export async function getGeoJSON(): Promise<FeatureCollection | null> {
  const token = await getAccessToken()!
  
  const response = await fetch(`${process.env.API_URL}/secured/map/features`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    console.error('Falha ao obter GeoJSON')

    if (response.status == 401) {
      redirect('/')
    }
    return null
  }
  
  const polygons = await response.json()
  return polygons as FeatureCollection
}


export async function getSoilUsage(): Promise<SoilUsage[]> {
  const token = await getAccessToken()!

  const response = await fetch(`${process.env.API_URL}/secured/map/soil_usage`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    console.error('Falha ao obter GeoJSON')

    if (response.status == 401) {
      redirect('/')
    }
    return []
  }
  
  const soils = await response.json()
  return soils as SoilUsage[]
}