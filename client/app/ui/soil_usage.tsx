'use client'
import type { SoilUsage } from "../actions/map";

export default function SoilList(
  state: { 
    soils: SoilUsage[],
    onSoilSelect: (soil: SoilUsage) => void
  }
) {
  return <details open={true}>
    <summary className="text-xl cursor-pointer bg-gray-100 hover:bg-gray-200 text-gray-900 px-4 py-2">Usos do solo</summary>
    <div className="px-4">
      <div>
        <ul className="py-4">
          {state?.soils.map((soil: SoilUsage) => (
            <li
              className="border-b border-gray-300 align-middle py-2 cursor-pointer hover:bg-gray-100"
              key={soil.desc_uso_solo}
              onClick={() => state.onSoilSelect(soil)}
              role="button"
            >
              <span
                className={`inline-block w-4 h-4 mr-2`}
                style={{
                  backgroundColor: soil.rgb
                }}
              ></span>
              {soil.desc_uso_solo}
            </li>
          ))}
        </ul>
      </div>
    </div>
  </details>
}