# Customise this file, documentation can be found here:
# https://github.com/fastlane/fastlane/tree/master/fastlane/docs
# All available actions: https://github.com/fastlane/fastlane/blob/master/fastlane/docs/Actions.md
# can also be listed using the `fastlane actions` command

# Change the syntax highlighting to Ruby
# All lines starting with a # are ignored when running `fastlane`

# If you want to automatically update fastlane if a new version is available:
# update_fastlane

# This is the minimum version number required.
# Update this, if you use features of a newer version
fastlane_version "2.9.0"
build_gradle_file_path = File.expand_path("..", Dir.pwd)+"/automapgs/build.gradle"

class FileHelper
      def self.read(path)
        file = File.open(path, "r+")
        res = file.read
        file.close
        res
      end
      def self.write(path, str)
          require 'fileutils.rb'
          FileUtils.makedirs(File.dirname(path))
          file = File.open(path, "w+")
          file.write(str)
          file.close
      end
end

#fastlane has not option to execute gradle task with params (22.05.17)
def gradleWithParam(args)
    task = args[:task]
    paramName = args[:paramName]
    paramValue = args[:paramValue]
    gradle(task: "-P#{paramName}=#{paramValue} #{task}")
end

default_platform :android

platform :android do
  before_all do
    #create AppFile
    FileHelper.write(Dir.pwd + '/Appfile', 'json_key_file "' + ENV['json_key_file'] + "\"\n" + 'package_name "' + ENV['app_id'] + '"')
    unless ENV["metadata_dir"].nil?
      system ("mv " + ENV["metadata_dir"] + " metadata")
      UI.important("Use custom ITC metadata.")
    end
  end

  module BuildState
      START = 1
      SUCCESS = 2
      FAILURE = 3
  end


  def sendJobState(projectAlias, cmd, state, message = nil)
    require 'net/http'
    require 'uri'
    require 'json'

    uri = URI.parse("http://mobile.geo4.io/bot/releaseBuilder/jobStates")
    data = {"alias":projectAlias,"cmd":cmd,"state":state}

    if message != nil
        data['message'] = message
    end

    # Create the HTTP objects
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri.request_uri)
    request['Content-Type'] = 'application/json'
    request.body = data.to_json

    # Send the request
    response = http.request(request)
    puts "------REQUEST------"
    puts request.body
    puts response
  end

  def generateReleaseNotes(cmd, project_alias, version, lang = nil)
    cmnd = cmd
    if lang != nil
       cmnd = cmnd+lang
    else
       raise "Language is required for release notes generating."
    end
    gs_get_release_notes(cmd: cmnd,
       lang: lang,
       alias: project_alias,
       displayVersionName: version)
    UI.message("Check exist " + Dir.pwd + "/../../../notes/" + project_alias + "/" + version + "_" + lang + ".txt")
    if !File.exist?(Dir.pwd + "/../../../notes/" + project_alias + "/" + version + "_" + lang + ".txt")
        raise "Не удалось сгенерировать ReleaseNotes"
    end
  end

  desc "Submit a new Beta Build to Crashlytics"
  lane :beta do
    # Increment the build number (not the version number)
    gradle(task: "incrementVersionCode" + ENV["versionsFilePostfix"])
    gradle(task: "incrementBetaVersionName" + ENV["versionsFilePostfix"])
    text = FileHelper.read(build_gradle_file_path)
    version_name = text.match(/currentVersionName = '(.*)'/)[1]

    generateReleaseNotes("fileBeta", ENV['alias'], version_name, "Ru")
    generateReleaseNotes("fileBeta", ENV['alias'], version_name, "En")

    ruText = FileHelper.read(Dir.pwd + "/../../../notes/" + ENV["alias"] + "/" + version_name + "_Ru.txt")
    enText = FileHelper.read(Dir.pwd + "/../../../notes/" + ENV["alias"] + "/" + version_name + "_En.txt")

    require 'date'
    current_time = DateTime.now
    time_string = current_time.strftime "%d.%m.%Y %H-%M"
    crashlytics_changelog = time_string + "\n" + ruText + "\n\n" + enText
    UI.message("changelog = " + crashlytics_changelog)

    gradle(task: "clean")
    gradle(task: "assemble", flavor: ENV["flavor"], build_type: "Beta")
    crashlytics(
       notes: crashlytics_changelog,
       groups: ENV["test_group_for_fabric"]
    )

    gradleWithParam(task: "saveVersionCode", paramName: "versionsFilePostfix", paramValue: ENV["versionsFilePostfix"])
    gradleWithParam(task: "saveBetaVersionName", paramName: "versionsFilePostfix", paramValue: ENV["versionsFilePostfix"])
  end



  desc "Deploy a new RC version to the Google Play"
  lane :rc do
    gradle(task: "incrementVersionCode" + ENV["versionsFilePostfix"])
    gradle(task: "incrementRcVersionName" + ENV["versionsFilePostfix"])
    text = FileHelper.read(build_gradle_file_path)
    version_name = text.match(/currentVersionName = '(.*)'/)[1]

    ruNotesFilePath = Dir.pwd + "/../../../notes/" + ENV['versionsFilePostfix'] + "/" + version_name + "_Ru.txt"
    enNotesFilePath = Dir.pwd + "/../../../notes/" + ENV['versionsFilePostfix'] + "/" + version_name + "_En.txt"

    if !File.exist?(ruNotesFilePath) || !File.exist?(enNotesFilePath)
        generateReleaseNotes("fileClosed", ENV['versionsFilePostfix'], version_name, "Ru")
        generateReleaseNotes("fileClosed", ENV['versionsFilePostfix'], version_name, "En")
    end

    ruText = FileHelper.read(ruNotesFilePath)
    enText = FileHelper.read(enNotesFilePath)

    version_code = text.match(/versionCode (.*)/)[1]

    FileHelper.write(Dir.pwd+'/metadata/android/ru-RU/changelogs/'+ version_code +'.txt', ruText)
    FileHelper.write(Dir.pwd+'/metadata/android/en-US/changelogs/'+ version_code +'.txt', ruText)

    gradle(task: "clean")
    gradle(task: "assemble", flavor: ENV["flavor"], build_type: "Release")
    supply(track: "beta", skip_upload_metadata: true, skip_upload_images: true, skip_upload_screenshots: true)

    gradleWithParam(task: "saveVersionCode", paramName: "versionsFilePostfix", paramValue: ENV["versionsFilePostfix"])
    gradleWithParam(task: "saveRcVersionName", paramName: "versionsFilePostfix", paramValue: ENV["versionsFilePostfix"])
  end



  desc "Deploy release version to Google Play"
  lane :release do
    supply(track: "beta", track_promote_to: "production", skip_upload_apk: true, skip_upload_metadata: true, skip_upload_images: true, skip_upload_screenshots: true)
    gradleWithParam(task: "saveReleaseVersionName", paramName: "versionsFilePostfix", paramValue: ENV["versionsFilePostfix"])
  end



  after_all do |lane|
     text = FileHelper.read(build_gradle_file_path)
     version_name = text.match(/currentVersionName = '(.*)'/)[1]

     cmd = ""
     options = {}
     if lane == :beta
        cmd = "beta"
        options = {cmd:cmd,
           displayVersionName:version_name,
           request: "cmd",
           alias: ENV["alias"]
        }
     elsif lane == :rc
        cmd = "mv2rc"
        options = {cmd:cmd,
           displayVersionName:version_name,
           request: "cmd",
           alias: ENV["alias"]
        }
     elsif lane == :release
        cmd = "rc2release"
        options = {cmd:cmd,
           displayVersionName:version_name,
           request: "cmd",
           alias: ENV["alias"]
        }
     end
     if cmd != ""
        gs_execute_command(options)
     end
     sendJobState(ENV['alias'], lane, 'successful')
  end

  error do |lane, exception|
     text = FileHelper.read(build_gradle_file_path)
     version_name = text.match(/currentVersionName = '(.*)'/)[1]

     message = ENV["project_name"] + " " + version_name + " build has failed. Reason:\n" + exception.message

     puts message

     sendJobState(ENV['alias'], lane, 'failed', message)
  end
end