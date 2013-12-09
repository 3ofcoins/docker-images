require 'bundler/setup'

require 'docker'
require 'erubis'
require 'minigit'

ENV['REGISTRY'] ||= 'localhost:5000'
ENV['PUBLIC_REGISTRY'] ||= ENV['REGISTRY']
ENV['MAINTAINER'] ||= 'Maciej Pasternacki <maciej@3ofcoins.net>'

class DockerImageTask < Rake::Task
  def initialize(*)
    super
    enhance([dockerfile_task], &:build!)
    self.comment = "#{repository}:#{tag}"
  end

  def dockerfile_task
    if File.exist? dockerfile_template
      Rake::FileTask.define_task(dockerfile => dockerfile_template) do |t|
        puts "# rendering #{t}"
        File.write(dockerfile, Erubis::Eruby.new(File.read(dockerfile_template)).result(binding))
      end
    else
      Rake::FileTask.define_task(dockerfile)
    end
  end

  def build!(task=nil)
    puts "# Building #{self}"
    @image = Docker::Image.build_from_dir(name)
    puts "# tag #{repository}:#{tag} #{repository}:latest"
    image.tag('repo' => "#{repository}:#{tag}")
    image.tag('repo' => repository)
  end

  def needed?
    dirty? || !image
  end

  def image
    @image ||= Docker::Image.all.find { |img| img.info['Repository'] == repository && img.info['tag'] == sha1 }
  end

  def tag
    @docker_tag ||= sha1
  end

  def repository
    "#{ENV['REGISTRY']}/#{File.basename(name)}"
  end

  def dockerfile
    "#{name}/Dockerfile"
  end

  def dockerfile_template
    "#{dockerfile}.erb"
  end

  def sha1
    git.rev_list({max_count: 1}, 'HEAD', '--', name).strip
  end

  def dirty?
    !git.status({porcelain: true}, name).empty?
  end

  def git
    @git ||= MiniGit::Capturing.new(name)
  end
end

desc 'All Docker images'
task :images

Dir['**/Dockerfile*'].map { |df| File.dirname(df) }.uniq.each do |dir|
  task :images => DockerImageTask.define_task(dir)
end

task :pry do
  require 'pry'
  binding.pry
end
