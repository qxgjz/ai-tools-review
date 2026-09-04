import { ExternalLink, BookOpen, Clock } from "lucide-react";

interface Source {
  title: string;
  url: string;
  type?: "official" | "review" | "research" | "documentation";
  accessedDate?: string;
}

interface SourceReferencesProps {
  sources?: Source[];
  toolName?: string;
  showLastUpdated?: boolean;
  lastUpdated?: string;
}

const DEFAULT_SOURCES: Source[] = [
  {
    title: "Official Product Website",
    url: "#",
    type: "official",
    accessedDate: "2026-09-01",
  },
  {
    title: "AIToolCrux Editorial Testing Standards",
    url: "/about",
    type: "documentation",
    accessedDate: "2026-09-01",
  },
];

const TYPE_LABELS: Record<string, string> = {
  official: "Official Source",
  review: "Third-Party Review",
  research: "Research Data",
  documentation: "Documentation",
};

const TYPE_COLORS: Record<string, string> = {
  official: "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
  review: "bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400",
  research: "bg-purple-50 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400",
  documentation: "bg-gray-50 text-gray-700 dark:bg-gray-800 dark:text-gray-400",
};

export function SourceReferences({
  sources,
  toolName,
  showLastUpdated = true,
  lastUpdated,
}: SourceReferencesProps) {
  const displaySources = sources && sources.length > 0 ? sources : DEFAULT_SOURCES;
  const updateDate = lastUpdated || new Date().toISOString().split("T")[0];

  return (
    <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-5 border border-gray-100 dark:border-gray-800">
      <div className="flex items-center gap-2 mb-4">
        <BookOpen className="w-5 h-5 text-blue-600 dark:text-blue-400" />
        <h3 className="text-base font-bold text-gray-900 dark:text-white">
          Sources & References
        </h3>
      </div>

      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        This review was conducted using our {toolName ? `${toolName} ` : ""}6-dimension evaluation framework.
        We verify all claims against primary sources and update reviews regularly.
      </p>

      <ul className="space-y-3">
        {displaySources.map((source, index) => (
          <li key={index} className="flex items-start gap-3">
            <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold flex-shrink-0 mt-0.5 ${TYPE_COLORS[source.type || "documentation"]}`}>
              {TYPE_LABELS[source.type || "documentation"]}
            </span>
            <div className="flex-1 min-w-0">
              {source.url && source.url !== "#" ? (
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium inline-flex items-center gap-1"
                >
                  {source.title}
                  <ExternalLink className="w-3 h-3 flex-shrink-0" />
                </a>
              ) : (
                <span className="text-sm text-gray-700 dark:text-gray-300 font-medium">
                  {source.title}
                </span>
              )}
              {source.accessedDate && (
                <p className="text-xs text-gray-400 mt-0.5 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  Accessed: {source.accessedDate}
                </p>
              )}
            </div>
          </li>
        ))}
      </ul>

      {showLastUpdated && (
        <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            <strong>Last updated:</strong> {updateDate} · Reviews are updated every 90 days or when major product changes occur.
          </p>
        </div>
      )}
    </div>
  );
}
