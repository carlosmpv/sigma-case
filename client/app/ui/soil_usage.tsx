import type { SoilUsage } from "../actions/map";




export default function SoilUsage(state: { soils: SoilUsage[] }) {
  return <details open>
    <summary className="text-xl cursor-pointer bg-gray-200 p-2">Usos do solo</summary>
    <div className="px-4">
      <div>
        <ul className="py-4">
          {state?.soils.map((soil: SoilUsage) => (
            <li
              className="border-b border-gray-300 align-middle py-2"
              key={soil.desc_uso_solo}
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