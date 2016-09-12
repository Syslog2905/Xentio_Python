Feature: Transcoder service

 
  @HUB-576 @HUB-577 @assignee:ben.dalby @COMPLETED @TRANSCODER
  Scenario Outline: Create job and poll using all roles

    When as a <role> I upload the video <video_file>, type <video_type> to the transcoder service (API)
    And as a <role> I poll for the last started job until it is completed (API)
    Then the status of the transcoder job is completed (API)
    Then the output with key video.mp4 is present (API)
    And  the output with key hls_0400k/video is present (API)
    And  the output with key hls_0600k/video is present (API)
    And  the output with key hls_1000k/video is present (API)
    And  the output with key hls_1500k/video is present (API)
    And  the playlist with name video is present (API)
        Examples:
         | role          | video_file | video_type |
         | blippar_user  | video.mp4  | video/mp4  |
         | normal_user   | video.mp4  | video/mp4  |
         | group_admin   | video.mp4  | video/mp4  |
         | blippar_admin | video.mp4  | video/mp4  |

