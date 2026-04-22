export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <p className="text-sm text-muted">© 2026 Scheme Explainer. All rights reserved.</p>
          <div className="flex space-x-6 text-sm text-muted">
            <a 
              href="https://github.com/Meghana-Chakravarthi/ai-scheme-explainer#readme" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:text-[#1E293B] transition-colors"
            >
              Privacy
            </a>
            <a 
              href="https://github.com/Meghana-Chakravarthi/ai-scheme-explainer#readme" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:text-[#1E293B] transition-colors"
            >
              Terms
            </a>
            <a 
              href="https://github.com/Meghana-Chakravarthi/ai-scheme-explainer/issues" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:text-[#1E293B] transition-colors"
            >
              Contact
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
