@Entity
@Table(name="user_feed")
public class Post implements Serializable {

    @Id
    @Column(name="user_id")
    private long mUserId;

    @Column(name="is_repost")
    private boolean mIsRepost;

    @Column(name="date_created")
    private Date mDateCreated;

    @OneToOne
    @JoinColumn(name="poll_id")
    private Poll mPoll;

    // Aggiunta di una relazione OneToMany con Comment
    @OneToMany(mappedBy = "post", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Comment> comments;

}

@Entity
@Table(name="poll")
public class Poll implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long mId;

    @Column(name="user_id")
    private long mUserId;

    @Column(name="question")
    private String mQuestion;

    @Column(name="date_created")
    private Date mDateCreated;
}

// Nuova entità Comment
@Entity
@Table(name="comment")
public class Comment implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long mId;

    @Column(name="user_id")
    private long mUserId;

    @Column(name="content")
    private String mContent;

    @Column(name="date_created")
    private Date mDateCreated;

    // Relazione ManyToOne con Post
    @ManyToOne
    @JoinColumn(name="post_id", nullable = false)
    private Post post;

}
