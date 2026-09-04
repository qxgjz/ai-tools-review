import Link from "next/link";
import { User, Twitter, Linkedin, Github, Globe } from "lucide-react";

interface AuthorBioProps {
  name?: string;
  role?: string;
  bio?: string;
  avatar?: string;
  showLinks?: boolean;
}

export function AuthorBio({
  name = "AIToolCrux Editorial Team",
  role = "AI Tools Expert & Reviewer",
  bio = "Our editorial team has 8+ years of experience testing and reviewing AI tools. We conduct hands-on testing, compare features across 6 dimensions, and update reviews regularly to ensure you get the most accurate and up-to-date recommendations.",
  avatar,
  showLinks = true,
}: AuthorBioProps) {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 rounded-xl p-5 border border-gray-100 dark:border-gray-800">
      <div className="flex items-start gap-4">
        {/* 作者头像 */}
        <div className="flex-shrink-0">
          {avatar ? (
            <img
              src={avatar}
              alt={name}
              className="w-14 h-14 rounded-full object-cover ring-2 ring-blue-500/20"
            />
          ) : (
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xl font-bold shadow-lg shadow-blue-500/20">
              {name.charAt(0).toUpperCase()}
            </div>
          )}
        </div>

        {/* 作者信息 */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h4 className="text-base font-bold text-gray-900 dark:text-white">{name}</h4>
            <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-[10px] font-semibold">
              <User className="w-3 h-3 mr-1" />
              Verified Expert
            </span>
          </div>
          <p className="text-sm text-blue-600 dark:text-blue-400 font-medium mt-0.5">{role}</p>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 leading-relaxed">{bio}</p>

          {/* 链接 */}
          {showLinks && (
            <div className="flex items-center gap-3 mt-3">
              <Link
                href="/about"
                className="text-xs text-blue-600 dark:text-blue-400 hover:underline font-medium inline-flex items-center gap-1"
              >
                <Globe className="w-3 h-3" />
                View Full Profile
              </Link>
              <a
                href="https://twitter.com/aitoolcrux"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-blue-500 transition-colors"
                aria-label="Twitter"
              >
                <Twitter className="w-4 h-4" />
              </a>
              <a
                href="https://linkedin.com/company/aitoolcrux"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-blue-700 transition-colors"
                aria-label="LinkedIn"
              >
                <Linkedin className="w-4 h-4" />
              </a>
              <a
                href="https://github.com/qxgjz"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
                aria-label="GitHub"
              >
                <Github className="w-4 h-4" />
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
