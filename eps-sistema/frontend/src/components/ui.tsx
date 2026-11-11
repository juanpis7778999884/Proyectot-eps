export function Table({ columns, data, rowKey = "id" }: any) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
      <table className="w-full text-left text-sm">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((col: any) => (
              <th key={col.key} className="px-4 py-3 font-medium text-gray-700 uppercase tracking-wider">
                {col.label}
              </th>
            ))}
            <th className="px-4 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.map((row: any) => (
            <tr key={row[rowKey]} className="hover:bg-gray-50">
              {columns.map((col: any) => (
                <td key={col.key} className="px-4 py-3 text-gray-800">
                  {typeof col.render === "function" ? col.render(row) : row[col.key]}
                </td>
              ))}
              <td className="px-4 py-3">{row.actions}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function Badge({ children, variant = "default" }: any) {
  const base = "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium";
  const styles: Record<string, string> = {
    default: "bg-gray-100 text-gray-700",
    success: "bg-green-100 text-green-700",
    warning: "bg-yellow-100 text-yellow-700",
    danger: "bg-red-100 text-red-700",
    info: "bg-blue-100 text-blue-700",
  };
  return (
    <span className={base + " " + styles[variant]}>{children}</span>
  );
}

export function Input({ label, ...props }: any) {
  return (
    <div className="mb-4">
      {label && <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>}
      <input {...props} className="w-full rounded border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-eps-500 focus:border-eps-500 outline-none" />
    </div>
  );
}

export function Button({ children, variant = "primary", ...props }: any) {
  const base = "inline-flex items-center justify-center rounded px-4 py-2 text-sm font-semibold outline-none transition";
  const styles: Record<string, string> = {
    primary: "bg-eps-600 text-white hover:bg-eps-700 focus:ring-2 focus:ring-eps-500",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    danger: "bg-red-600 text-white hover:bg-red-700",
    ghost: "bg-transparent text-gray-600 hover:bg-gray-100",
  };
  return (
    <button className={base + " " + styles[variant]} {...props}>
      {children}
    </button>
  );
}

export function Card({ children, className = "" }: any) {
  return (
    <div className={`rounded-xl border border-gray-200 bg-white p-6 shadow-sm ${className}`}>
      {children}
    </div>
  );
}

export function Alert({ children, variant = "info" }: any) {
  const styles: Record<string, string> = {
    error: "bg-red-50 border-red-200 text-red-800",
    success: "bg-green-50 border-green-200 text-green-800",
    info: "bg-blue-50 border-blue-200 text-blue-800",
    warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
  };
  return (
    <div className={`rounded border p-4 mb-4 text-sm ${styles[variant]}`}>{children}</div>
  );
}
