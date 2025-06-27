class Dashtrash < Formula
  include Language::Python::Virtualenv

  desc "Terminal-based dashboard for real-time monitoring"
  homepage "https://github.com/turancannb02/dashtrash"
  url "https://files.pythonhosted.org/packages/source/d/dashtrash/dashtrash-0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"
  head "https://github.com/turancannb02/dashtrash.git", branch: "main"

  depends_on "python@3.11"

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-14.0.0.tar.gz"
    sha256 "82f1bc23a6a21ebca4ae0c45af9bdbc492ed20231dcb63f297d6d1021a9d5725"
  end

  resource "psutil" do
    url "https://files.pythonhosted.org/packages/source/p/psutil/psutil-7.0.0.tar.gz"
    sha256 "3f02134e82cfb5d089fddf6df5c6afacf50fd195d65a9a00a5f166e0fc86fcbc"
  end

  resource "pyfiglet" do
    url "https://files.pythonhosted.org/packages/source/p/pyfiglet/pyfiglet-1.0.3.tar.gz"
    sha256 "4e8a8c14e3e1ba3de18e72ad7b7abf93e6c3474b8efdd5bb1725f3ace5d3e6dd"
  end

  resource "PyYAML" do
    url "https://files.pythonhosted.org/packages/source/P/PyYAML/PyYAML-6.0.2.tar.gz"
    sha256 "d584d9ec91ad65861cc08d42e834324ef890a082e591037abe114850ff7bbc3e"
  end

  resource "textual" do
    url "https://files.pythonhosted.org/packages/source/t/textual/textual-3.5.0.tar.gz"
    sha256 "11c7bffac684b6abba9fe28c8f21b5df0b8b2e84e9db8b6c4b4b3f3d2b6a6c7a"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"dashtrash", "--help"
    system bin/"dashtrash", "--version"
    system bin/"dashtrash", "--create-config"
  end
end 