class Dashtrash < Formula
  desc "Real-time terminal dashboard with questionable aesthetics"
  homepage "https://github.com/turancannb02/dashtrash"
  url "https://github.com/turancannb02/dashtrash/archive/refs/heads/main.tar.gz"
  version "1.0.0"
  sha256 :no_check  # We'll update this after first release
  license "MIT"

  depends_on "python@3.12"

  def install
    # Install Python dependencies
    system Formula["python@3.12"].opt_bin/"python3", "-m", "pip", "install", 
           "--target=#{libexec}", "psutil", "pyfiglet", "rich"
    
    # Install the package
    system Formula["python@3.12"].opt_bin/"python3", "-m", "pip", "install", 
           "--target=#{libexec}", "."
    
    # Create wrapper script
    (bin/"dashtrash").write <<~EOS
      #!/bin/bash
      export PYTHONPATH="#{libexec}:$PYTHONPATH"
      exec "#{Formula["python@3.12"].opt_bin}/python3" -m dashtrash "$@"
    EOS
  end

  test do
    system "#{bin}/dashtrash", "--help"
  end
end 